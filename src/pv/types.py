#
#  Piano Video
#  Piano MIDI visualizer
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import io
import struct
import time
import numpy as np
from typing import Any, Dict, IO, List, Tuple, Type, Union
from .utils import UI32, get
from .props import Property


class Operator:
    idname: str
    label: str
    description: str = ""

    args: List[Property] = []

    def __str__(self) -> str:
        return f"pv.types.Operator(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, attr: str) -> Any:
        """
        Returns argument value from self.args list.
        """
        return get(self.args, attr).value

    def poll(self) -> bool:
        return True

    def execute(self) -> str:
        return "FINISHED"

    def report(self, type: str, message: str) -> None:
        import pv
        pv.context.report = (type, f"{message}")
        pv.context.report_time = time.time()


class OpCaller:
    """
    Positioned at pv.ops.<group>.<caller>
    Calls an operator. Takes in kwargs and sets them in
    the operator call.
    """
    operator: Type[Operator]
    idname: str

    def __init__(self, op: Type[Operator]) -> None:
        self.operator = op
        self.idname = op.idname.split(".")[1]

    def __str__(self) -> str:
        return f"pv.types.OpCaller(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, **kwargs) -> str:
        op = self.operator()
        for key in kwargs:
            prop = get(op.args, key, raise_error=False)
            if prop is None:
                raise ValueError(f"Could not find prop with idname {key}")
            prop.value = kwargs[key]

        try:
            cleared = op.poll()
        except:
            op.report("ERROR", "Poll failed")
            return "CANCELLED"

        if cleared:
            return op.execute()
        return "CANCELLED"


class OpGroup:
    """
    Positioned at pv.ops.<group>
    Has a group of callers.
    """
    callers: List[OpCaller]
    idname: str

    def __init__(self, idname: str) -> None:
        self.callers = []
        self.idname = idname

    def __str__(self) -> str:
        return f"pv.types.OpGroup(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, attr: str) -> OpCaller:
        return get(self.callers, attr)


class Ops:
    """
    The Operators submodule pv.ops
    """
    groups: List[OpGroup]

    def __init__(self) -> None:
        self.groups = []

    def __str__(self) -> str:
        return f"pv.types.Ops()"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, attr: str) -> OpGroup:
        return get(self.groups, attr)


class Function:
    idname: str
    label: str
    description: str = ""

    def __str__(self) -> str:
        return f"pv.types.Function(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()

    def execute(self, *args, **kwargs) -> Any:
        ...


class FuncCaller:
    """
    Positioned at pv.funcs.<group>.<caller>
    Calls a function's execute method.
    """
    function: Type[Function]
    idname: str

    def __init__(self, func: Type[Function]) -> None:
        self.function = func
        self.idname = func.idname.split(".")[1]

    def __str__(self) -> str:
        return f"pv.types.FuncCaller(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, *args, **kwargs) -> str:
        op = self.function()
        return op.execute(*args, **kwargs)


class FuncGroup:
    """
    Positioned at pv.funcs.<group>
    Has a group of callers.
    """
    callers: List[FuncCaller]
    idname: str

    def __init__(self, idname: str) -> None:
        self.callers = []
        self.idname = idname

    def __str__(self) -> str:
        return f"pv.types.FuncCaller(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, attr: str) -> FuncCaller:
        return get(self.callers, attr)


class Funcs:
    """
    The Functions submodule pv.funcs
    """
    groups: List[FuncGroup]

    def __init__(self) -> None:
        self.groups = []

    def __str__(self) -> str:
        return f"pv.types.Funcs()"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, attr: str) -> FuncGroup:
        return get(self.groups, attr)


class PropertyGroup:
    idname: str
    props: List[Property]

    def __str__(self) -> str:
        return f"pv.types.PropertyGroup(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, attr: str) -> Any:
        """
        Returns the value of the prop, not the property itself.
        """
        return get(self.props, attr).value

    def __setattr__(self, attr: str, value: Any) -> None:
        """
        Sets prop with idname "name" to "value"
        """
        get(self.props, attr).value = value

    def get(self, attr: str) -> Property:
        """
        Returns the property with idname attr.
        """
        return get(self.props, attr)

    def dump(self, stream: IO[bytes]) -> None:
        """
        Writes number of props as unsigned 32 bit integer.
        Then, writes header and data for each prop.
        """
        stream.write(struct.pack(UI32, len(self.props)))
        for prop in self.props:
            prop.dump_header(stream)
            prop.dump(stream)

    def load(self, stream: io.BytesIO) -> None:
        """
        Loads number of props.
        Then reads header and calls load on each corresponding prop.
        Will raise ValueError if a type ID is incorrect.
        """
        num_props = struct.unpack(UI32, stream.read(4))[0]
        for _ in range(num_props):
            type_id = stream.read(1)[0]
            idname = stream.read(struct.unpack(UI32, stream.read(4))[0]).decode()
            for prop in self.props:
                if prop.idname == idname:
                    if prop.type_id != type_id:
                        raise ValueError(f"Incorrect type ID on {self.idname}.{idname}:" + \
                            f"Expected {prop.type_id}, got {type_id} from stream.")
                    prop.load(stream)
                    break


class UILayout:
    """
    A layout class, which can be drawn on to show props, operators, etc.
    """
    elements: List[Dict[str, Any]]

    def __init__(self) -> None:
        self.elements = []

    def __str__(self) -> str:
        return f"pv.types.UILayout()"

    def __repr__(self) -> str:
        return self.__str__()

    def label(self, text: str = "") -> None:
        """
        Adds text.
        """
        self.elements.append({"type": "LABEL", "text": text})

    def prop(self, idpath: str, text: str = None, on_set: str = None) -> None:
        """
        Adds a property.
        :param idpath: ID name path of property (ex. "my_group.my_prop")
        :param text: Display this text next to the prop (set to None to use prop default)
        :param on_set: Operator path to run when this value is changed (ex. "my_group.my_op")
        """
        if idpath.count(".") != 1:
            raise ValueError(f"ID path must have exactly 1 period: {idpath}")
        if on_set is not None and on_set.count(".") != 1:
            raise ValueError(f"Operator path must have exactly 1 period: {on_set}")
        self.elements.append({"type": "PROP", "idpath": idpath, "text": text, "on_set": on_set})

    def operator(self, idpath: str, text: str = None, kwargs: Dict[str, Any] = {}) -> None:
        """
        Adds an operator.
        :param idpath: ID name path of operator (ex. "my_group.my_prop")
        :param text: Display this text next to the operator (set to None to use operator default)
        """
        if idpath.count(".") != 1:
            raise ValueError(f"ID path must have exactly 1 period: {idpath}")
        self.elements.append({"type": "OPERATOR", "idpath": idpath, "text": text, "kwargs": kwargs})


class UIPanel:
    idname: str
    label: str
    description: str
    section_id: str

    layout: UILayout
    expanded: bool

    def __init__(self) -> None:
        self.layout = UILayout()
        self.expanded = False

    def __str__(self) -> str:
        return f"pv.types.UIPanel(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()

    def draw(self) -> None:...


class UISection:
    idname: str
    label: str
    description: str
    icon: str

    icon_img: Union[np.ndarray, None]
    panels: List[UIPanel]

    def __init__(self):
        self.icon = ""
        self.icon_img = None
        self.panels = []

    def __str__(self) -> str:
        return f"pv.types.UISection(idname={self.idname})"

    def __repr__(self) -> str:
        return self.__str__()


class Scene:
    pgroups: List[PropertyGroup]

    def __init__(self) -> None:
        self.pgroups = []

    def __str__(self) -> str:
        return f"pv.types.Scene()"

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(self, attr: str) -> PropertyGroup:
        return get(self.pgroups, attr)


class Context:
    scene: Scene

    ui_sections: List[UISection]
    operators: List[Operator]

    report: Union[Tuple[str, str], None]    # (type, message)
    report_time: float

    def __init__(self) -> None:
        self.scene = Scene()

        self.ui_sections = []
        self.operators = []

        self.report = None
        self.report_time = 0

    def __str__(self) -> str:
        return f"pv.types.Context()"

    def __repr__(self) -> str:
        return self.__str__()
