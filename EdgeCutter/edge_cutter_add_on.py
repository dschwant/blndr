######################################################
# Still to do:
# - internal document
# - fix starting_? to current location
# - make rotation axis choice work
# 
######################################################

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
from bpy.types import Scene
from bpy.props import EnumProperty, IntProperty
from math import radians

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
		box = layout.box()
		box.label("Set Values:")
		row = box.row()
		
		row.prop_search(scene, "Target", bpy.data, "objects",icon="TRIA_DOWN")
		row = box.row()
		row.prop_search(scene, "Cutter", bpy.data, "objects",icon="TRIA_DOWN")
		row = box.row()
		# row.prop(scene, "RotAxis", text="Rotation Axis")
		# row = box.row()
		row.prop(scene, "NumSteps", text="Num. Steps")
		row = box.row()
		row.prop(scene, "LimSteps", text="Stop at Step")
		box = layout.box()
		row = box.row(False)
		row.operator("cutter.cut", text="Do Cuts")	
	
class OBJECT_CutButton(bpy.types.Operator):
	bl_idname = "cutter.cut"
	bl_label = "Make Cuts"
	country = bpy.props.StringProperty()
	
	def execute(self, context):
		vars = context.scene
		coin = bpy.data.objects[vars.Target]
		cutter = bpy.data.objects[vars.Cutter]
		get_Euler = coin.rotation_euler
		print(get_Euler)
		starting_Z = 0
		stepRads = radians(360 / vars.NumSteps)

		for i in range(0, vars.LimSteps):
			coin.rotation_euler = (0,0,starting_Z)
			bpy.ops.object.select_all(action='DESELECT')
			coin.select = True
			bpy.context.scene.objects.active = coin
			bpy.ops.object.modifier_add(type='BOOLEAN')
			mod = coin.modifiers
			mod[0].name = "CutEdge"
			mod[0].operation = 'DIFFERENCE'
			mod[0].object = cutter
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod[0].name)
			starting_Z=starting_Z + stepRads
			i += 1
		
		if self.country == '':
			print(context.scene.Target)
			print(context.scene.Cutter)
			# print(context.scene.RotAxis)
			print(get_Euler)
			print(context.scene.NumSteps)
			print(context.scene.LimSteps)
			print("Make Cuts")
		else:
			print("Don't Make Cuts from %s!" % self.country)
		return {"FINISHED"}

def register():
	bpy.utils.register_class(ToolsPanel)
	bpy.utils.register_class(OBJECT_CutButton)
	Scene.Target = bpy.props.StringProperty()
	Scene.Cutter = bpy.props.StringProperty()
	Scene.RotAxis = EnumProperty(items=(('1', "X", "Rotate on X axis"),
                                          ('2', "Y", "Rotate on Y axis"),
                                          ('3', "Z", "Rotate on Z axis")),
                                   name="Rotation Axis",
                                   description="Axis on which to rotate Target for cuts.")
	Scene.NumSteps = IntProperty(name='Number of Steps', min=2, max=360, description="Number steps to devide full 360deg rotation into.")
	Scene.LimSteps = IntProperty(name='Limit number of Steps', min=2, max=360, description="Number steps to stop at.")

def unregister():
	bpy.utils.unregister_class(ToolsPanel)
	bpy.utils.unregister_class(OBJECT_CutButton)
	del bpy.types.Object.Target
	del bpy.types.Object.Cutter
	del bpy.types.Object.RotAxis

if __name__ == "__main__":
	register()