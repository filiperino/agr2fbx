bl_info = {
    "name": "agr2fbx",
    "category": "Import-Export",
    "author": "filiperino",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "description": "huj",
    "location": "File > Import/Export"
    }

import bpy

class agr2fbx(bpy.types.Operator):
    """Exports AGR players with "player" string to FBX format"""   # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "export_scene.agr2fbx"        # unique identifier for buttons and menu items to reference.
    bl_label = "AGR (.fbx)"        # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    
    # Properties used by the file browser
    filepath = bpy.props.StringProperty(subtype="DIR_PATH")
    
    def menu_draw_export(self, context):
        layout = self.layout
        layout.operator("export_scene.agr2fbx", text="AGR (.fbx)")
    
    # Open the filebrowser with the custom properties
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    # main function
    def execute(self, context):
        # change filepath, if something is inputted in the File Name Box
        if not self.filepath.endswith("\\"):
            self.filepath = self.filepath.rsplit(sep="\\", maxsplit=1)[0] + "\\"
                
        # select and rename hierarchy objects to root
        for CurrentModel in bpy.data.objects:
            if CurrentModel.name.find("player") != -1:
                # select root
                CurrentModel.select = True
                # select children
                for CurrentChildren in CurrentModel.children:
                    CurrentChildren.select = True
                # rename top to player
                CurrentObjectName = CurrentModel.name
                CurrentModel.name = "root"
                # export current object as fbx
                fullfiles = self.filepath + "/" + CurrentObjectName + ".fbx"  
                bpy.ops.export_scene.fbx(
                    filepath = fullfiles, 
                    use_selection = True, 
                    bake_anim_use_nla_strips = False, 
                    bake_anim_use_all_actions = False, 
                    bake_anim_simplify_factor = 0,
                    add_leaf_bones=False)
                # undo all changes
                CurrentModel.name = CurrentObjectName
                CurrentModel.select = False
                for CurrentChildren in CurrentModel.children:
                    CurrentChildren.select = False

            # export camera
        if bpy.data.objects.find("afxCam") != -1:
            bpy.data.objects["afxCam"].select = True
            fullfiles = self.filepath + "/afxcam.fbx"
            bpy.ops.export_scene.fbx(filepath = fullfiles, use_selection = True, bake_anim_use_nla_strips = False, bake_anim_use_all_actions = False, bake_anim_simplify_factor = 0, object_types={'CAMERA'}, add_leaf_bones=False)
            bpy.data.objects["afxCam"].select = False
            return {'FINISHED'}



def register():
    bpy.utils.register_class(agr2fbx)
    bpy.types.INFO_MT_file_export.append(agr2fbx.menu_draw_export)
    
def unregister():
    bpy.types.INFO_MT_file_export.remove(agr2fbx.menu_draw_export)
    bpy.utils.unregister_class(agr2fbx)

if __name__ == "__main__":
    register()
