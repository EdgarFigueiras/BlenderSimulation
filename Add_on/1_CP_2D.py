bl_info = {    
    "name": "Particles calculator",    
    "category": "Object",
}

import bpy
import time
import math
import random
import numpy as np
from scipy import interpolate
from scipy.interpolate import spline

class ParticleCalculator(bpy.types.Operator):
    """My Object Moving Script"""                 # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "particle.calculator"             # unique identifier for buttons and menu items to reference.
    bl_label = "Particle calculator"              # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}             # enable undo for the operator.
   
    def execute(self,context):        # execute() is called by blender when running the operator.
       
        #To calculate the amplittude of the particle is made the average of the 3 datas from the diferent axis
        def calculate_amplittude (p_x, p_y, p_z): 
            ampl = p_x + p_y + p_z
            ampl = ampl / 3
            ampl = int(ampl * 10)   #This only take the first digit at the left of the dot, by this way the system to create the particles with diferent colour becomes normalized 

            return ampl

        #Define an error message if occurs a problem during the run, is showed using a popup 
        def error_message(self, context):
            self.layout.label("No datafile selected. Remember to select a compatible datafile")

        bpy.context.space_data.viewport_shade = 'MATERIAL'
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()
        bpy.context.scene.frame_current = 0    
        bpy.data.scenes["Scene"].my_tool.int_box_state = -1
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)   #Refresh the actual visualization with the new generator object placed  

        #Reading the data to generate the function who originated it
        #Read the data from te panel 
        path = bpy.data.scenes['Scene'].my_tool.path #Origin from where the data will be readen, selected by the first option in the Panel
        
        try:
            file_with_data_files = open(path, 'r+')
            line = file_with_data_files.readline()

            for cnt in range(0,int(line)):
                file = file_with_data_files.readline()
                file = file.split("\n")

                file_with_binary_data = open(file[0], 'rb+') #File with binary data
            
                #Creating a file to save the particles placement information, helps to avoid a problem with Blender wich moves particles random
                file_with_particles_data = open(path + '.particles_info' + str(cnt), 'wb+')

                array_with_all_data = np.load(file_with_binary_data) #Gets the binary data as an array with 6 vectors (x_data, x_probability, y_data, y_probability, z_data, z_probability)
           
                #Matrix with the data of the 2D grid
                Z = array_with_all_data['arr_0'] 
                N = len(Z[0])   #Size of the matrix

                particles_number = bpy.data.scenes['Scene'].my_tool.int_box_n_particulas #Read from the panel 
                
                #Vectors which will store the data of x and y positions 
                xs = np.random.randint(N, size=particles_number) #xs[N]={0-n_points,...,N-2,0-n_points}
                ys = np.random.randint(N, size=particles_number) 
                zs = [0 for x in range(particles_number)]

                lista = [] #Array where all data will be stored

                rand_aux = 0
                rand_bool = False
                x_aux=0
                y_aux=0

                #Calculate the coordinates of each particle
                for cont in range(particles_number):
                    rand_bool = False
                    while not rand_bool:
                        x_aux = np.random.randint(0, N)
                        y_aux = np.random.randint(0, N)
                        rand_aux = np.random.uniform(0, 1)
                        if(rand_aux < Z[x_aux][y_aux]):
                            x_pos = x_aux - N/2
                            y_pos = y_aux - N/2
                            z_pos = np.random.uniform(0, 1) * 10
                            rand_bool = True
                            #ampl = calculate_amplittude(amplX, amplY, amplZ)
                            lista.append((x_pos, y_pos, z_pos, x_pos, y_pos, z_pos, x_pos))    #All the data is stored together


                #Top down sorting using amplittude before calculated as the element to sort 
                lista.sort(key=lambda lista: lista[6], reverse=True)    #Sort the list placing the data with bigger amplittude at the top

                np.savez(file_with_particles_data,lista)
                    
                #Zbpy.context.scene.frame_current = bpy.context.scene.frame_current + 1   #Goes one frame forward to show particles clear at rendering MANDATORY
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)             #Redraws to show particles new placement MANDATORY

                file_with_binary_data.close()
                file_with_particles_data.close()

        except:
            bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')


        bpy.ops.particle.generation() #Next step, go to particle generation

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

# ------------------------------------------------------------------------
#    Register and unregister functions
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(ParticleCalculator)


def unregister():
    bpy.utils.unregister_class(ParticleCalculator)
    
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()   
