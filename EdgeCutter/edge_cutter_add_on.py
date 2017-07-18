bl_info = {
    "name": "Edge_Rotate_Cutter",
    "author": "DS",
    "version": (0,0,1),
    "description": "Does boolean difference on an object in circlular pattern",
    "location": "View3D > Tool Shelf > ERCutter",
    "warning": "",
    "category": "Object"}

import bpy
import math
from mathutils import Vector
from functools import reduce

class ToolsPanel(bpy.types.Panel):
    bl_label = "Edge Rotate Cutter"
    bl_idname = "VIEW_3D_TOOLS_Edge_Rotate_Cutter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Cutter"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.prop_search(scene, "Cutter", scene, "objects")
        col.operator("cutter.cut", text="Do Cuts")

class OBJECT_CutButton(bpy.types.Operator):
    bl_idname = "cutter.cut"
    bl_label = "Make Cuts"
    country = bpy.props.StringProperty()
 
    def execute(self, context):
        if self.country == '':
            print(context.scene.Cutter)
            print("Make Cuts")
        else:
            print("Don't Make Cuts from %s!" % self.country)
        return {"FINISHED"}

def register():
    bpy.utils.register_class(ToolsPanel)
    bpy.utils.register_class(OBJECT_CutButton)
    bpy.types.Scene.Cutter = bpy.props.StringProperty()


def unregister():
    bpy.utils.unregister_class(ToolsPanel)
    bpy.utils.unregister_class(OBJECT_CutButton)
    del bpy.types.Object.Cutter

if __name__ == "__main__":
    register()