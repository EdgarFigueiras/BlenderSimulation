bl_info = {    
    "name": "Particles Stabilizer",    
    "category": "Object",
}

import bpy
import time
import math
import random
import struct
import binascii
import numpy as np

class ParticlesStabilizer(bpy.types.Operator):
    """My Object Moving Script"""               # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "particle.stabilizer"           # unique identifier for buttons and menu items to reference.
    bl_label = "Particles Stabilization"        # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}           # enable undo for the operator.
   
    def execute(self,context):        # execute() is called by blender when running the operator.

        #Define an error message if occurs a problem during the run, is showed using a popup
        def error_message(self, context):
            self.layout.label("Imposible to stabilize particles. Try to Run simulation again")

        #return the name of the emitter wich is asigned to this number by order
        def emitter_system(x):
            if x == 0 : 
                emitter = bpy.data.objects['Sphere']
            if (x > 0 and x < 10) :
                emitter = bpy.data.objects['Sphere.00' + str(x)]
            if (x >= 10 and x < 100) :
                emitter = bpy.data.objects['Sphere.0' + str(x)]
            return emitter.particle_systems[-1] 

        
        try:
            path = bpy.data.scenes['Scene'].my_tool.path
            file_with_data_files = open(path, 'r+')
            line = file_with_data_files.readline()
            file_with_data_files.close()
        except:
            bpy.context.window_manager.popup_menu(error_message, title="An error ocurred reading from the original file", icon='CANCEL')


        for cnt in range(0,int(line)):
            try:
                file_with_particles_data = open(path + '.' + str(cnt) + '.particles_places.txt', 'r+')
                
                #Emitter, use the same Sphere or increase it 
                x=cnt
                psys1 = emitter_system(x)   

                for pa in psys1.particles:

                    line = file_with_particles_data.readline()
                    x_pos,y_pos,z_pos,residual = line.split(" ") 
                                   
                    xx = (float(x_pos))
                    yy = (float(y_pos))
                    zz = (float(z_pos))

                    #God´s particle solution
                    #if pa.die_time < 500 :
                    pa.die_time = 500
                    pa.lifetime = 500
                    pa.velocity = (0,0,0)

                    pa.location = (xx,yy,zz)

                ##x = x+1


                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                #Make the scene go one frame forward MANDATORY
                bpy.context.scene.frame_current = bpy.context.scene.frame_current + 1

                file_with_particles_data.close()

            except:
                bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')

            #bpy.context.scene.frame_current = bpy.context.scene.frame_current + 1
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

# ------------------------------------------------------------------------
#    Register and unregister functions
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(ParticlesStabilizer)


def unregister():
    bpy.utils.unregister_class(ParticlesStabilizer)
    
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()   
