#
#  Piano Video
#  A free piano visualizer.
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

__all__ = (
    "PropertyGroup",
    "DataGroup",
    "Cache",
    "Operator",
    "OpGroup",
    "Job",
)

import os
import json
from typing import IO, Any, Dict, List, Sequence, TYPE_CHECKING
from .props import Property

Video = None
if TYPE_CHECKING:
    from pvkernel import Video


class PropertyGroup:
    """
    A collection of Properties.

    When creating your own PropertyGroup, you will inherit a class from
    this base class. Then, define:

    * ``idname``: The unique idname of this property group.
    * properties: Define each property as a static attribute (shown below).

    .. code-block:: py

        class MyProps(pv.PropertyGroup):
            prop1 = pv.props.BoolProp(name="hi")
    """
    idname: str

    def __getattribute__(self, name: str) -> Any:
        attr = object.__getattribute__(self, name)
        if isinstance(attr, Property):
            return attr.value
        else:
            return attr

    def __setattr__(self, name: str, value: Any) -> None:
        self._get_prop(name).value = value

    def _get_prop(self, name: str) -> Property:
        """
        You can use this to bypass ``__getattribute__`` and get the
        actual Property object.
        """
        return object.__getattribute__(self, name)


class DataGroup:
    """
    A group of data pointers.

    When creating your own DataGroup, inherit and define the idname.

    Then, you can run ``video.data_idname.value = x`` or ``video.data_idname.value2``
    to access and set values.

    The values can be any type.
    Value names cannot be ``idname`` or ``items``, as they will overwrite internal variables.
    """
    idname: str
    items: Dict[str, Any]

    def __init__(self):
        self.items = {}

    def __getattr__(self, name: str) -> Any:
        return object.__getattribute__(self, "items")[name]

    def __setattr__(self, name: str, value: Any) -> None:
        if not hasattr(self, "items"):
            object.__setattr__(self, "items", {})
        object.__getattribute__(self, "items")[name] = value

class Cache:
    """
    Cache managing for a video.

    You can read and write specific file names with ``cache.fp(name, mode)``,
    or automatically set the name to the current frame with ``cache.fp_frame``.

    To add a cache, inherit and define:

    * ``idname``: Cache idname. Will also be the cache folder name.
    * ``depends``: Tuple of property idnames this cache depends on.
      If any of them change, the cache will be cleared. Default ``()``.
    """
    idname: str
    depends: Sequence[str] = ()

    def __init__(self, video: Video):
        self.path = os.path.join(video.cache, self.idname)

        self._video = video
        self._state = os.path.join(self.path, ".state.json")
        self._frames = []

        os.makedirs(self.path, exist_ok=True)

    def fp(self, name: str, mode: str) -> IO:
        """
        Get the file pointer for a file name.
        """
        return open(os.path.join(self.path, name), mode)

    def fp_frame(self, mode: str, check_exist: bool = True) -> IO:
        """
        Get the file pointer for the current frame.
        Internal frame list will be updated.
        """
        self._check_state()

        frame = self._video.frame
        if mode.startswith("w") and frame not in self._frames:
            self._frames.append(frame)
        elif mode.startswith("r") and frame not in self._frames and check_exist:
            raise ValueError(f"Frame {frame} does not exist in cache.",
                "Pass argument check_exist=False to override.")

        return open(os.path.join(self.path, str(frame)), mode)

    def _check_state(self):
        from .utils import multigetattr

        if os.path.isfile(self._state):
            with open(self._state, "r") as fp:
                props = json.load(fp)["props"]
            for attr in self.depends:
                if multigetattr(self._video.props, attr) != props[attr]:
                    self._frames = []

        info = {
            "props": {name: multigetattr(self._video.props, name) for name in self.depends},
        }
        with open(self._state, "w") as fp:
            json.dump(info, fp, indent=4)


class Operator:
    """
    A function that is positioned at ``pv.ops.group.idname``.
    It can be displayed in the GUI.

    The return value will always be None.

    To create your own operator, inherit and define:

    * ``group``: Operator group.
    * ``idname``: Unique operator idname.
    * ``label``: The text that will show on the GUI (as a button).
    * ``description``: What this operator does.
    * ``execute(video)``: This will be run when the operator is called.
      The first parameter is the video class (``pvkernel.Video``)
    """
    group: str
    idname: str
    label: str
    description: str

    def __init__(self, video: Video) -> None:
        self._video = video

    def __call__(self) -> None:
        self.execute(self._video)

    def execute(self, video: Video) -> None:
        ...

class OpGroup:
    """
    Internal class.
    Positioned at ``pv.ops.group``
    """
    idname: str
    operators: List[Operator]
    video: Video

    def __init__(self, idname: str, video: Video) -> None:
        self.idname = idname
        self.operators = []
        self.video = video

    def __getattr__(self, name: str) -> Operator:
        from .utils import get
        return get(self.operators, name)


class Job:
    """
    Create a job to modify the final video.

    See https://piano-video.rtfd.io/en/latest/blog/render_jobs.html for more info.

    Inherit and define:

    * ``idname``: Job idname.
    * ``ops``: List of operator idnames (``"group.idname"``) to run.
    """
    idname: str
    ops: List[str]
