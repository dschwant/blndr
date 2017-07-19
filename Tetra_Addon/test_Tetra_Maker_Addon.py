######################################################
# Originally from https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Addon_User_Interface
# To Do:
# - make it so you can choose dimensions
# - add steps to clean up after create.
######################################################

bl_info = {
	"name": "Add_Mesh_Tetrahedron",
	"author": "DS",
	"version": (0,0,1),
	"description": "Adds tetrahedron",
	"location": "View3D > Tool Shelf > Create",
	"warning": "",
	"category": "Object"}
import math
import bpy
import mathutils

class TetrahedronMakerPanel(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_context = "objectmode"
	bl_category = "Create"
	bl_label = "Add Tetrahedron"
	
	def draw(self, context):
		TheCol = self.layout.column(align=True)
		TheCol.operator("mesh.make_tetrahedron", text="Add Tetrahedron")
	#end draw

#end TetrahedronMakerPanel

class MakeTetrahedron(bpy.types.Operator):
	bl_idname = "mesh.make_tetrahedron"
	bl_label = "Add Tetrahedron"
	bl_options = {"UNDO"}
	
	def invoke(self, context, event):
		Vertices = [mathutils.Vector((0, -1 / math.sqrt(3),0)),
			mathutils.Vector((0.5, 1 / (2 * math.sqrt(3)), 0)),
			mathutils.Vector((-0.5, 1 / (2 * math.sqrt(3)), 0)),
			mathutils.Vector((0, 0, math.sqrt(2 / 3))),]
		NewMesh = bpy.data.meshes.new("Tetrahedron")
		NewMesh.from_pydata (Vertices,
				[],
				[[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]])
		NewMesh.update()
		NewObj = bpy.data.objects.new("Tetrahedron", NewMesh)
		context.scene.objects.link(NewObj)
		return {"FINISHED"}
	#end invoke

#end MakeTetrahedron

def register():
	bpy.utils.register_class(MakeTetrahedron)
	bpy.utils.register_class(TetrahedronMakerPanel)

def unregister():
	bpy.utils.register_class(MakeTetrahedron)
	bpy.utils.register_class(TetrahedronMakerPanel)

if __name__ == "__main__":
	register()