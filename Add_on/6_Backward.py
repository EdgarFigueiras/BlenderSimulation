bl_info = {    
    "name": "Particles Backward",    
    "category": "Object",
}

import bpy
import time
import math
import random
import struct
import binascii
import numpy as np

class ParticlesBackward(bpy.types.Operator):
    """My Object Moving Script"""               # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "particle.backward"           # unique identifier for buttons and menu items to reference.
    bl_label = "Particles Backward"        # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}           # enable undo for the operator.
   
    def execute(self,context):        # execute() is called by blender when running the operator.
    #Define an error message if occurs a problem during the run, is showed using a popup
        def error_message(self, context):
            self.layout.label("Imposible to read from original file. Try to Run simulation again")

        def draw(self, context):
            self.layout.label("Returned to the origin state")

        try:
            path = bpy.data.scenes['Scene'].my_tool.path
            file_with_data_files = open(path, 'r+')
            total_states = file_with_data_files.readline()
            file_with_data_files.close()
        except:
            bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')

        actual_state = bpy.data.scenes["Scene"].my_tool.int_box_state 


        #First time do this
        if(actual_state == -1):
            for cnt in range(0, int(total_states)):
                nombreObjeto = "Sphere"
                if (cnt>0 and cnt<10):
                    nombreObjeto = "Sphere.00" + str(cnt)
                if (cnt>10 and cnt<100):
                    nombreObjeto = "Sphere.0" + str(cnt) 
                bpy.data.objects[nombreObjeto].hide = True

            bpy.data.objects["Sphere"].hide = False
            bpy.data.scenes["Scene"].my_tool.int_box_state = 0
        
        else:
            #If is not the last state
            if((actual_state-1) >= 0):
                #Take the name of the Sphere to make the complete name and disable it
                nombreObjeto="Sphere"
                nombreObjetoSiguiente="Sphere"

                if (actual_state>0 and actual_state<10):
                    nombreObjeto = "Sphere.00" + str(actual_state)
                if ((actual_state-1)>0 and (actual_state-1)<10):
                    nombreObjetoSiguiente = "Sphere.00" + str(actual_state-1)

                if (actual_state>=10 and actual_state<100):
                    nombreObjeto = "Sphere.0" + str(actual_state)
                if ((actual_state-1)>=10 and (actual_state-1)<100):
                    nombreObjetoSiguiente = "Sphere.0" + str(actual_state-1)

                bpy.data.objects[nombreObjeto].hide = True
                bpy.data.objects[nombreObjetoSiguiente].hide = False

                bpy.data.scenes["Scene"].my_tool.int_box_state = actual_state - 1

            if((actual_state-1) < 0):
                nombreObjeto="Sphere"
                numeroObjetoSiguiente = int(total_states)-1

                if (numeroObjetoSiguiente>0 and numeroObjetoSiguiente<10):
                    nombreObjeto = "Sphere.00" + str(numeroObjetoSiguiente)

                if (numeroObjetoSiguiente>=10 and numeroObjetoSiguiente<100):
                    nombreObjeto = "Sphere.0" + str(numeroObjetoSiguiente)

                bpy.data.objects[nombreObjeto].hide = False
                bpy.data.objects["Sphere"].hide = True

                bpy.data.scenes["Scene"].my_tool.int_box_state = numeroObjetoSiguiente

                #bpy.context.window_manager.popup_menu(draw, title="Returned to begin", icon='ARROW_LEFTRIGHT')






        return {'FINISHED'}            # this lets blender know the operator finished successfully.

# ------------------------------------------------------------------------
#    Register and unregister functions
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(ParticlesBackward)


def unregister():
    bpy.utils.unregister_class(ParticlesBackward)
    
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()   
