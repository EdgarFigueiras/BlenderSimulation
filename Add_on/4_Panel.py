import bpy
import time
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

# ------------------------------------------------------------------------
#    Panel which allows the user to interact with the simulator
# ------------------------------------------------------------------------

#Clean the scene
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()


image_format = (
    ('BMP', 'BMP', ''),
    ('IRIS', 'IRIS', ''),
    ('PNG', 'PNG', ''),
    ('JPEG', 'JPEG', ''),
    ('JPEG2000', 'JPEG2000', ''),
    ('TARGA', 'TARGA', ''),
    ('TARGA_RAW', 'TARGA_RAW', ''), 
    ('CINEON', 'CINEON', ''),
    ('DPX', 'DPX', ''),
    ('OPEN_EXR_MULTILAYER', 'OPEN_EXR_MULTILAYER', ''),
    ('OPEN_EXR', 'OPEN_EXR', ''), 
    ('HDR', 'HDR', ''),
    ('TIFF', 'TIFF', '')
)

video_format = (
    ('AVI_JPEG', 'AVI_JPEG', ''),
    ('AVI_RAW', 'AVI_RAW', ''), 
    ('FRAMESERVER', 'FRAMESERVER', ''), 
    ('H264', 'H264', ''),
    ('FFMPEG', 'FFMPEG', ''),
    ('THEORA', 'THEORA', '')
)

enum_items = (
    ('FOO', 'Foo', ''),
    ('BAR', 'Bar', '')
)

class MySettings(PropertyGroup):

    path = StringProperty(
        name="Data File",
        description="Select the file with the simulation data.",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')

    image_path = StringProperty(
        name="Store Path",
        description="Path where renders will be stored, by default uses the path of the simulation data",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')

    int_box_n_particulas = IntProperty(
        name="Particles N ", 
        description="Total number of particles of the simulation",
        min = 50, max = 4000,
        default = 150)

    int_box_granularity = IntProperty(
        name="Granularity ", 
        description="Modifies the granularity. Min = 1 , Max = 10",
        min = 1, max = 10,
        default = 5)

    int_box_saturation = IntProperty(
        name="Saturation ", 
        description="Modify the saturation. Min = 1, Max = 10",
        min = 1, max = 10,
        default = 5)

    int_box_state = IntProperty(
        name="State ", 
        description="Modify the State",
        min = -1, max = 999,
        default = -1)
     
 
class OBJECT_OT_ResetButton(bpy.types.Operator):
    bl_idname = "reset.image"
    bl_label = "Reiniciar entorno"
    country = bpy.props.StringProperty()

    def execute(self, context):

        def confirm_message(self, context):
            self.layout.label("The system environment was cleaned")

        #Delete all the created Spheres
        try:
            path = bpy.data.scenes['Scene'].my_tool.path
            file_with_data_files = open(path, 'r+')
            total_spheres = file_with_data_files.readline()
            file_with_data_files.close()
        except:
            bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')


        for cnt in range(0, int(total_spheres)):
            nombreObjeto = "Sphere"
            if (cnt>0 and cnt<10):
                nombreObjeto = "Sphere.00" + str(cnt)
            if (cnt>=10 and cnt<100):
                nombreObjeto = "Sphere.0" + str(cnt)         

            bpy.data.objects[nombreObjeto].hide = False

        bpy.context.space_data.viewport_shade = 'MATERIAL'
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()
        bpy.context.scene.frame_current = 0

        bpy.data.scenes["Scene"].my_tool.int_box_state = -1
        bpy.context.window_manager.popup_menu(confirm_message, title="Reset", icon='VIEW3D_VEC')

        return{'FINISHED'} 



class OBJECT_OT_RenderButton(bpy.types.Operator):
    bl_idname = "render.image"
    bl_label = "RenderizarImagen"
    country = bpy.props.StringProperty()


    #This code 
    def execute(self, context):

        dir_image_path = bpy.data.scenes['Scene'].my_tool.image_path

        #Define an error message if occurs a problem during the run, is showed using a popup
        def error_message(self, context):
            self.layout.label("Unable to save the Render. Try again with other path")


        try:    
            #Set the image format, PNG by default
            bpy.context.scene.render.image_settings.file_format = bpy.context.scene['ImageFormat']

        except:        
            bpy.context.scene.render.image_settings.file_format = 'PNG'

        try:

            #Sets the path where the file will be stored, by default the same as the datafile
            if dir_image_path == "":
                bpy.data.scenes['Scene'].render.filepath = bpy.data.scenes['Scene'].my_tool.path + time.strftime("%c%s") + '.jpg'
                
                #Define a confirmation message to the default path            
                def confirm_message(self, context):
                    self.layout.label("Render image saved at: " + bpy.data.scenes['Scene'].my_tool.path )

            else:                
                bpy.data.scenes['Scene'].render.filepath = dir_image_path + time.strftime("%c%s") + '.jpg'
               
                #Define a confirmation message to the selected path 
                def confirm_message(self, context):
                    self.layout.label("Rendered image saved at: " + dir_image_path )   

            bpy.ops.render.render( write_still=True ) 


            bpy.context.window_manager.popup_menu(confirm_message, title="Saved successful", icon='SCENE')

        except:
            bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')

        return{'FINISHED'} 


#Renders all objects one by one jumping between states
class OBJECT_OT_RenderAllButton(bpy.types.Operator):
    bl_idname = "render_all.image"
    bl_label = "RenderizarAllImagen"
    country = bpy.props.StringProperty()


    #This code 
    def execute(self, context):

        dir_image_path = bpy.data.scenes['Scene'].my_tool.image_path

        #Define an error message if occurs a problem during the run, is showed using a popup
        def error_message(self, context):
            self.layout.label("Unable to save the Renders. Try again with other path")

        #Open the file to know hom many renders will do
        try:
            path = bpy.data.scenes['Scene'].my_tool.path
            file_with_data_files = open(path, 'r+')
            total_states = file_with_data_files.readline()
            file_with_data_files.close()
        except:
            bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')

        for x in range(int(total_states)):

            try:    
                #Set the image format, PNG by default
                bpy.context.scene.render.image_settings.file_format = bpy.context.scene['ImageFormat']

            except:        
                bpy.context.scene.render.image_settings.file_format = 'PNG'

            try:

                #Sets the path where the file will be stored, by default the same as the datafile
                if dir_image_path == "":
                    bpy.data.scenes['Scene'].render.filepath = bpy.data.scenes['Scene'].my_tool.path + str(x) + '.jpg'
                    
                    #Define a confirmation message to the default path            
                    def confirm_message(self, context):
                        self.layout.label("Render image saved at: " + bpy.data.scenes['Scene'].my_tool.path )

                else:                
                    bpy.data.scenes['Scene'].render.filepath = dir_image_path + str(x) + '.jpg'
                   
                    #Define a confirmation message to the selected path 
                    def confirm_message(self, context):
                        self.layout.label("Rendered image saved at: " + dir_image_path )   

                bpy.ops.render.render( write_still=True ) 

                bpy.ops.particle.forward()
                

            except:
                bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')


        bpy.context.window_manager.popup_menu(confirm_message, title="Saved successful", icon='SCENE')

        return{'FINISHED'} 


class OBJECT_OT_RenderVideoButton(bpy.types.Operator):
    bl_idname = "render.video"
    bl_label = "RenderizarVideo"
    country = bpy.props.StringProperty()


    #This code 
    def execute(self, context):

        dir_image_path = bpy.data.scenes['Scene'].my_tool.image_path

        #Define an error message if occurs a problem during the run, is showed using a popup
        def error_message(self, context):
            self.layout.label("Unable to save the Render. Try again with other path")


        try:    
            #Set the video format, AVI_JPEG by default            
            bpy.context.scene.render.image_settings.file_format = bpy.context.scene['VideoFormat'] 

        except:        
            bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG' 
        
        try:

            #Sets the path where the file will be stored, by default the same as the datafile
            if dir_image_path == "":
                bpy.data.scenes['Scene'].render.filepath = bpy.data.scenes['Scene'].my_tool.path + time.strftime("%c%s") + '.avi'
                
                #Define a confirmation message to the default path            
                def confirm_message(self, context):
                    self.layout.label("Rendered video saved at: " + bpy.data.scenes['Scene'].my_tool.path )

            else:                
                bpy.data.scenes['Scene'].render.filepath = dir_image_path + time.strftime("%c%s") + '.avi'
               
                #Define a confirmation message to the selected path 
                def confirm_message(self, context):
                    self.layout.label("Rendered video saved at: " + dir_image_path )   

            bpy.ops.render.render(animation=True, write_still=True )


            bpy.context.window_manager.popup_menu(confirm_message, title="Saved successful", icon='SCENE')

        except:
            bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')

        return{'FINISHED'}
      


class OBJECT_PT_my_panel(Panel):
    bl_idname = "OBJECT_PT_my_panel"
    bl_label = "Simulation Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = "objectmode"

class Panel(bpy.types.Panel):
    """Panel para añadir al entorno 3D"""
    bl_label = "Simulation Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column(align=True)
        box1 = layout.box()
        box2 = layout.box()
        box22 = layout.box()
        box3 = layout.box()
        box4 = layout.box()
       
        box1.label(text="PARAMETERS")

        box1.label(text="Select the data file", icon='LIBRARY_DATA_DIRECT')

        box1.prop(scn.my_tool, "path", text="")

        box1.label(text="Select the number of particles", icon='PARTICLE_DATA')

        box1.prop(scn.my_tool, "int_box_n_particulas")

        box1.label(text="Select the granularity", icon='GROUP_VERTEX')

        box1.prop(scn.my_tool, "int_box_granularity")

        box1.label(text="Select the saturation", icon='GROUP_VCOL')

        box1.prop(scn.my_tool, "int_box_saturation")



        box2.label(text="SIMULATION")

        box2.operator("particle.calculator", text="Run Simulation")

        #box2.operator("particle.stabilizer", text="Place Particles")

        box2.operator("reset.image", text="Reset Environment")


        #Box to move back and forward between states

        box22.label(text="STATES")

        row_box = box22.row()

        row_box.prop(scn.my_tool, "int_box_state")

        row_box.enabled = False    

        row = box22.row()

        row.operator("particle.backward", text="Previous State", icon='BACK')

        row.operator("particle.forward", text="Next State", icon='FORWARD')



        box3.label(text="RENDER")

        box3.label(text="Select the folder to store renders")

        box3.prop(scn.my_tool, "image_path", text="")

        box3.label(text="Select the image format (PNG as default)", icon='SCENE')

        box3.prop_search(context.scene, "ImageFormat", context.scene, "imageformats", text="" , icon='OBJECT_DATA')

        box3.operator("render.image", text="Save image")

        box3.operator("render_all.image", text="Save all images")

        box3.label(text="Select the video format (AVI as default)", icon='RENDER_ANIMATION')

        box3.prop_search(context.scene, "VideoFormat", context.scene, "videoformats", text="" , icon='OBJECT_DATA')

        box3.operator("render.video", text="Save video")

        box4.label(text="SHORTCUTS")

        box4.label(text="To switch view press SHIFT + Z", icon='INFO')

        box4.label(text="To start the animation press ALT + A", icon='INFO')



        


# ------------------------------------------------------------------------
#    Register and unregister functions
# ------------------------------------------------------------------------

def rellenar_selectores(scene):
    bpy.app.handlers.scene_update_pre.remove(rellenar_selectores)
    scene.imageformats.clear()
    scene.videoformats.clear()

    for identifier, name, description in image_format:
        scene.imageformats.add().name = name

    for identifier, name, description in video_format:
        scene.videoformats.add().name = name


def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.imageformats = bpy.props.CollectionProperty(
            type=bpy.types.PropertyGroup
        )

    bpy.types.Scene.videoformats = bpy.props.CollectionProperty(
            type=bpy.types.PropertyGroup
        )

    bpy.types.Scene.ImageFormat = bpy.props.StringProperty()

    bpy.types.Scene.VideoFormat = bpy.props.StringProperty()

    bpy.app.handlers.scene_update_pre.append(rellenar_selectores)

    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)

    

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool
    del bpy.types.Scene.coll
    del bpy.types.Scene.coll_string

if __name__ == "__main__":
    register()
