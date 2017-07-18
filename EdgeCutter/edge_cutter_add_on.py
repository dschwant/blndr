import bpy
import math
from mathutils import Vector
from functools import reduce

bl_info = {
    "name": "Edge_Rotate_Cutter",
    "author": "DS",
    "version": (0,0,1),
    "description": "Does boolean difference on an object in circlular pattern",
    "location": "View3D > Tool Shelf > ERCutter",
    "warning": "",
    "category": "Object"}

class ToolsPanel(bpy.types.Panel):
    bl_label = "Edge Rotate Cutter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Cutter"
    def draw(self, context):
        self.layout.operator("cutter.cut")

class OBJECT_CutButton(bpy.types.Operator):
    bl_idname = "cutter.cut"
    bl_label = "Make Cuts"
    country = bpy.props.StringProperty()
 
    def execute(self, context):
        if self.country == '':
            print("Make Cuts")
        else:
            print("Don't Make Cuts from %s!" % self.country)
        return{'FINISHED'}   
    
def register():
    bpy.utils.register_class(ToolsPanel)
 
def unregister():
    bpy.utils.unregister_class(ToolsPanel)
 
if __name__ == "__main__":  # only for live edit.
    bpy.utils.register_module(__name__)