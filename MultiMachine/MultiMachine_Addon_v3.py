######################################################
# Still to do:
# - internal documentation
# - Take out debug prints to console
# - Add repeater
######################################################

bl_info = {
	"name": "Multi_Machine_v3",
	"author": "DS",
	"version": (0,0,1),
	"description": "Does boolean differences or unions on an target using an object (tool) in a parameter driven pattern (rotate or slide).",
	"location": "View3D > Tool Shelf > MultiMachine",
	"warning": "",
	"category": "Object"}
	
import bpy
import math
from bpy.types import Scene
from bpy.props import EnumProperty, IntProperty, FloatProperty
from math import radians
from mathutils import Vector, Euler
from operator import add

class ToolsPanel(bpy.types.Panel):
	bl_label = "Multi Machine"
	bl_idname = "VIEW_3D_TOOLS_Multi_Machine_v3"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "MM3"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout
		scene = context.scene

		box = layout.box()
		row = box.row()
		row.prop_search(scene, "Target", bpy.data, "objects",icon="TRIA_DOWN")
		row = box.row()
		row.prop_search(scene, "Tool", bpy.data, "objects",icon="TRIA_DOWN")
		row = box.row()
		row.prop(scene, "MMAction", text="Action")
		row = box.row()
		row.prop(scene, "MMMove", text="Move")
		row = box.row()
		row.prop(scene, "MMToolXVal", text="X")
		row = box.row()
		row.prop(scene, "MMToolYVal", text="Y")
		row = box.row()
		row.prop(scene, "MMToolZVal", text="Z")
		row = box.row()
		row.prop(scene, "NumSteps", text="Num. Steps")
		row = box.row()
		row.prop(scene, "StartSteps", text="Start at Step")
		row = box.row()
		row.prop(scene, "LimSteps", text="Stop at Step")

		box = layout.box()
		box.label("Pre-step:")
		row = box.row()
		row.prop(scene, "MMPreStep", text="Move")
		row = box.row()
		row.prop(scene, "MMPreStepXVal", text="X")
		row = box.row()
		row.prop(scene, "MMPreStepYVal", text="Y")
		row = box.row()
		row.prop(scene, "MMPreStepZVal", text="Z")
		row = box.row()

		box = layout.box() #
		row = box.row()
		row.prop(scene, "RepeaterCnt", text="Repeat")
		row = box.row()
		row.operator("tool.exec", text="Execute")
# End class ToolsPanel
	
class mmtoolButton(bpy.types.Operator):
	bl_idname = "tool.exec"
	bl_label = "Make Diff or Union"
	country = bpy.props.StringProperty()
	
	def execute(self, context):
		vars = context.scene
		target = bpy.data.objects[vars.Target]
		tool = bpy.data.objects[vars.Tool]
		get_Euler = target.rotation_euler
		get_Location = target.location
		print(get_Euler)
		print(get_Location)
		rot_loc = [get_Euler[0],get_Euler[1],get_Euler[2]]
		slide_loc = [get_Location[0],get_Location[1],get_Location[2]]
		toolRotRads = [radians(vars.MMToolXVal),radians(vars.MMToolYVal),radians(vars.MMToolZVal)]
		toolSlideUnits = [vars.MMToolXVal,vars.MMToolYVal,vars.MMToolZVal]
		prestepRotRads = [radians(vars.MMPreStepXVal),radians(vars.MMPreStepYVal),radians(vars.MMPreStepZVal)]
		prestepSlideUnits = [vars.MMPreStepXVal,vars.MMPreStepYVal,vars.MMPreStepZVal]

		print(context.scene.Target)
		print(context.scene.Tool)
		print(rot_loc)
		print(slide_loc)
		print(toolRotRads)
		print(toolSlideUnits)
		print(prestepRotRads)
		print(prestepSlideUnits)
		
		for r in range(0, vars.RepeaterCnt):
			if (vars.LimSteps > vars.NumSteps):
				vars.LimSteps = vars.NumSteps

			if (vars.MMPreStep =='Rotate'):
				print(vars.MMPreStep)
				rot_loc = [sum(z) for z in zip(rot_loc, prestepRotRads)]
			elif (vars.MMPreStep =='Slide'):
				print(vars.MMPreStep)
				slide_loc = [sum(z) for z in zip(slide_loc, prestepSlideUnits)]
			
			print(rot_loc)
			print(slide_loc)
			
			for i in range(0, vars.LimSteps+1):
				print(i)
				# target.rotation_euler = (rot_loc_X,rot_loc_Y,rot_loc_Z) # At step 0 this is the original location (or location after pre-step), else the location set at end of previous step
				# target.location = (slide_loc_X,slide_loc_Y,slide_loc_Z)
				# bpy.ops.object.select_all(action='DESELECT')
				# target.select = True
				# bpy.context.scene.objects.active = target
				
				# if (i >= vars.StartSteps): # Execute tool action at this step
					# bpy.ops.object.modifier_add(type='BOOLEAN')
					# mod = target.modifiers
					# mod[0].name = "MMTool"
					# if (vars.MMAction == 'Diff'):
						# mod[0].operation = 'DIFFERENCE'
					# else: # Assumes 'Union
						# mod[0].operation = 'UNION'
					# mod[0].object = tool
					# bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod[0].name)
					
				# if (vars.MMMove == 'Rotate'):
					# if vars.MMToolAxis == 'X':
						# rot_loc_X=rot_loc_X + stepRads
					# elif vars.MMToolAxis == 'Y':
						# rot_loc_Y=rot_loc_Y + stepRads
					# else: # Assumes 'Z'
						# rot_loc_Z=rot_loc_Z + stepRads
				# else: # Assumes 'Slide'
					# if vars.MMToolAxis == 'X':
						# slide_loc_X=slide_loc_X + vars.NumUnits
					# elif vars.MMToolAxis == 'Y':
						# slide_loc_Y=slide_loc_Y + vars.NumUnits
					# else: # Assumes 'Z'
						# slide_loc_Z=slide_loc_Z + vars.NumUnits
				i += 1
			r += 1
			
		if self.country == '':
			print('Done')
			# print(get_Euler)
			# print(context.scene.NumSteps)
			# print(context.scene.LimSteps)
			# print("Execute")
		else:
			print("Don't Make Cuts from %s!" % self.country)
		return {"FINISHED"}
# End class ToolsPanel

def register():
	bpy.utils.register_class(ToolsPanel)
	bpy.utils.register_class(mmtoolButton)
	Scene.Target = bpy.props.StringProperty()
	Scene.Tool = bpy.props.StringProperty()
	Scene.MMAction = EnumProperty(items=(('Diff', "Diff", "Do Boolean Difference"),
						('Union', "Union", "Do Boolean Union")),						
					name="Should the tool boolean diff or boolean union?",
					default = 'Diff',
					description="Action for the Multi Machine.")
	Scene.MMMove = EnumProperty(items=(('Slide', "Slide", "Slide the target on the axis"),
						('Rotate', "Rotate", "Rotate the target on the axis")),
					name="Movement for the tooling",
					default = 'Rotate',
					description="What action should happen in the machining sequence.")
	Scene.MMToolXVal = FloatProperty(name='MMToolXVal', default = 0, min=-100000, max=100000, description="Number of degrees or units to move target on X axis.")
	Scene.MMToolYVal = FloatProperty(name='MMToolYVal', default = 0, min=-100000, max=100000, description="Number of degrees or units to move target on Y axis.")
	Scene.MMToolZVal = FloatProperty(name='MMToolZVal', default = 0, min=-100000, max=100000, description="Number of degrees or units to move target on Z axis.")
	Scene.NumSteps = IntProperty(name='Number of Steps', min=1, max=10000, description="Number tooling steps to take.")
	Scene.StartSteps = IntProperty(name='Step to start tooling', min=0, max=10000, description="The step at which to start tooling (current location is zero).")
	Scene.LimSteps = IntProperty(name='Limit number of Steps', min=0, max=10000, description="Number step to stop at.")

	Scene.MMPreStep = EnumProperty(items=(('None', "None", "No Pre-step"),
						('Slide', "Slide", "Slide the target on the axis"),
						('Rotate', "Rotate", "Rotate the target on the axis")),
					name="MMPreStep",
					default = 'None',
					description="Movement for the Pre-step (done once before each tooling sequence).")
	Scene.MMPreStepXVal = FloatProperty(name='MMPreStepXVal', default = 0, min=-100000, max=100000, description="Number of degrees or units to move target on X axis in pre-step.")
	Scene.MMPreStepYVal = FloatProperty(name='MMPreStepYVal', default = 0, min=-100000, max=100000, description="Number of degrees or units to move target on Y axis in pre-step..")
	Scene.MMPreStepZVal = FloatProperty(name='MMPreStepZVal', default = 0, min=-100000, max=100000, description="Number of degrees or units to move target on Z axis in pre-step..")

	Scene.RepeaterCnt = IntProperty(name='RepeaterCnt', min=1, max=1000, description="Number of times to repeat the pre-step and tooling sequence.", default = 1)

def unregister():
	bpy.utils.unregister_class(ToolsPanel)
	bpy.utils.unregister_class(mmtoolButton)

if __name__ == "__main__":
	register()