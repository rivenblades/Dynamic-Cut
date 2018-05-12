#====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
#======================= END GPL LICENSE BLOCK =============================

bl_info = {
	'name': 'Dynamic Cutting edges',
	'description': "This add-ons allows to easily cut an edge with a technique of bevel and vertex group",
	'author': 'rivenblades',
	'version': (0, 0, 1),
	'blender': (2, 78, 0),
	'location': 'View3D > Tool > Cut & Go',
	'warning': '',
	"wiki_url": ""
				"",
	'tracker_url': '',
	'category': 'Cut & Go'}
import bpy
from bpy.types import Panel
class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
class VIEW3D_PT_tools_cut(View3DPanel, Panel):
    """Creates a Panel in the Object properties window"""
    bl_category = "Tools"
    bl_context = "objectmode"
    bl_label = "Cut & Go"
    
    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.operator("mesh.make_cut", text = "Cut")

class MakeCut(bpy.types.Operator) :
    bl_idname = "mesh.make_cut"
    bl_label = "Dynamic Cut"
    bl_options = {"UNDO"}
    

    def invoke(self, context, event) :
        vert_group_name = "Dynamic_Cut group_DO_NOT_TOUCH"
        counter = 0
        ob = bpy.context.selected_objects[0]
        active = bpy.context.active_object
        for i in range(0, len(active.vertex_groups)):
            counter += 1
        if counter >= 1 and vert_group_name in active.vertex_groups:
            print("there is a vertex group called " + vert_group_name)
        else:
            bpy.ops.object.vertex_group_add()
            bpy.context.active_object.vertex_groups['Group'].name = vert_group_name

        ## Add Bevel modifier
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].limit_method = 'VGROUP'
        bpy.context.object.modifiers["Bevel"].vertex_group = vert_group_name
        bpy.context.object.modifiers["Bevel"].segments = 2

        ## Add Vertex Weight modifier
        bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_EDIT')
        bpy.context.object.modifiers["VertexWeightEdit"].vertex_group = vert_group_name
        bpy.context.object.modifiers["VertexWeightEdit"].use_remove = True
        bpy.context.object.modifiers["VertexWeightEdit"].remove_threshold = 1

        ## Add Subsurf
        bpy.ops.object.modifier_add(type='SUBSURF')

        ## Add Mask modifier
        bpy.ops.object.modifier_add(type='MASK')
        bpy.context.object.modifiers["Mask"].vertex_group = vert_group_name
        bpy.context.object.modifiers["Mask"].invert_vertex_group = True
        bpy.context.object.name = "Split"
        
        bpy.context.object.modifiers["Bevel"].show_expanded = False
        bpy.context.object.modifiers["VertexWeightEdit"].show_expanded = False
        bpy.context.object.modifiers["Subsurf"].show_expanded = False
        bpy.context.object.modifiers["Mask"].show_expanded = False

        return {"FINISHED"}
    #end invoke



def register():
    bpy.utils.register_class(MakeCut)
    bpy.utils.register_class(VIEW3D_PT_tools_cut)


def unregister():
    bpy.utils.register_class(MakeCut)
    bpy.utils.unregister_class(VIEW3D_PT_tools_cut)


if __name__ == "__main__":
    register()
