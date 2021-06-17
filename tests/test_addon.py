pv_info = {
    "name": "test",
}

import pv
from pv.props import *


class TEST_PT_Props(pv.types.PropertyGroup):
    idname = "test"

    props = [
        BoolProp(
            idname="prop",
            label="A boolean property",
            description="hi"
        )
    ]


class TEST_UT_Section(pv.types.UISection):
    idname = "test"
    label = "A test"
    description = "..."


class TEST_UT_Panel(pv.types.UIPanel):
    idname = "test"
    label = "My Panel"
    description = "blahblahblah"
    section_id = "test"

    def draw(self):
        layout = self.layout
        layout.prop("test.prop")
        layout.label("This is a label")
        layout.operator("test.operator")


class TEST_OT_Operator(pv.types.Operator):
    idname = "test.operator"
    label = "An operator"
    description = "hi"

    def execute(self):
        self.report("INFO", "Ran the operator")
        return "FINISHED"


class TEST_DT_MyNamespace(pv.types.DataNamespace):
    idname = "test"
    data = {
        "hi": True,
    }


classes = (
    TEST_PT_Props,
    TEST_UT_Section,
    TEST_UT_Panel,
    TEST_OT_Operator,
    TEST_DT_MyNamespace,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)

def unregister():
    for cls in classes:
        pv.utils.unregister_class(cls)
