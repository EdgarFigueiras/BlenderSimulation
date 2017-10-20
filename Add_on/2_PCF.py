bl_info = {    
    "name": "Particles generation",    
    "category": "Object",
}

import bpy
import time
import math
import random
import struct
import binascii
import numpy as np

class ParticlesGenerator(bpy.types.Operator):
    """My Object Moving Script"""         # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "particle.generation"     # unique identifier for buttons and menu items to reference.
    bl_label = "Particles generation"     # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}     # enable undo for the operator.
   
    def execute(self,context):        # execute() is called by blender when running the operator.

        #Define a material
        def make_material(name, diffuse, specular, alpha):
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = diffuse
            mat.type = 'HALO'
            #Modify the granularity using the value from the panel in diferent properties
            mat.halo.size = 7 - (bpy.data.scenes['Scene'].my_tool.int_box_granularity/2)  #Moddifies the Halo size of the particles
            mat.diffuse_intensity = 0.01 * (bpy.data.scenes['Scene'].my_tool.int_box_granularity/2)
            mat.specular_color = specular
            mat.specular_intensity = 0.01 * (bpy.data.scenes['Scene'].my_tool.int_box_granularity/2)
            mat.alpha = alpha
            mat.ambient = 0.1 * (bpy.data.scenes['Scene'].my_tool.int_box_granularity/2)
            return mat

        #Reads the binary file with the data to create the number of generators and their particles
        def list_with_data(cnt):
            path = bpy.data.scenes['Scene'].my_tool.path
            file_with_particles_data = open(path + '.particles_info' + str(cnt), 'rb+')
            array_with_all_data = np.load(file_with_particles_data) #Gets the binary data as an array with 6 vectors (x_data, x_probability, y_data, y_probability, z_data, z_probability)
            lista = array_with_all_data['arr_0'] #Unpack all the data to a list like when it was created
            file_with_particles_data.close()
            return lista

        #Define an error message if occurs a problem during the run, is showed using a popup
        def error_message(self, context):
            self.layout.label("Unable to acces the _.particles_info.txt. Try to Run simulation again")

        def error_message2(self, context):
            self.layout.label("An error ocurred during the simulation, please try again")    

        def configure_particles(psys1):  
            # Emission    
            pset1 = psys1.settings
            pset1.name = 'DropSettings'
            pset1.normal_factor = 0.0
            pset1.object_factor = 1
            pset1.factor_random = 0
            pset1.frame_start = 0
            pset1.frame_end = bpy.context.scene.frame_current + 1
            pset1.lifetime = 500
            pset1.lifetime_random = 0
            pset1.emit_from = 'FACE'
            pset1.use_render_emitter = False
            pset1.object_align_factor = (0,0,0)
         
            pset1.count = particles_number    #number of particles that will be created with their own style

            # Velocity
            pset1.normal_factor = 0.0
            pset1.factor_random = 0.0
         
            # Physics
            pset1.physics_type = 'NEWTON'
            pset1.mass = 0
            pset1.particle_size = 5
            pset1.use_multiply_size_mass = False
         
            # Effector weights
            ew = pset1.effector_weights
            ew.gravity = 0
            ew.wind = 0
         
            # Children
            pset1.child_nbr = 0
            pset1.rendered_child_count = 0
            pset1.child_type = 'NONE'
         
            # Display and render
            pset1.draw_percentage = 100
            pset1.draw_method = 'CIRC'
            pset1.material = 1
            pset1.particle_size = 5  
            pset1.render_type = 'HALO'
            pset1.render_step = 0  

        #Blender saves the objects as "Sphere.xxx", where the "x" represents the number
        #It´s necesary a code to able the user to access objects every time the number changes
        #And this property is used to enable a diferent colour for the particles depending of the amplittude
        def set_colour(cont,me) :
            if cont==0:            
                nombreObjeto = "Sphere"
                ob = bpy.data.objects.get(nombreObjeto, me)
                ob.active_material = c9
            if (cont>0 and cont<10):
                nombreObjeto = "Sphere.00" + str(cont)
                ob = bpy.data.objects.get(nombreObjeto, me)
                if cont==1:
                    ob.active_material = c8
                if cont==2:
                    ob.active_material = c7
                if cont==3:
                    ob.active_material = c6
                if cont==4:
                    ob.active_material = c5
                if cont==5:
                    ob.active_material = c4
                if cont==6:
                    ob.active_material = c3
                if cont==7:
                    ob.active_material = c2
                if cont==8:
                    ob.active_material = c1
                if cont==9:
                    ob.active_material = c0
            if (cont>=10 and cont<100):
                nombreObjeto = "Sphere.0" + str(cont)
                ob = bpy.data.objects.get(nombreObjeto, me)


        #Changes the saturarion of the coulours from the value of the panel
        saturation = (bpy.data.scenes['Scene'].my_tool.int_box_saturation*0.05)
            
        #Materials created in function of their colour
        c0 = make_material('c0',(1,0,0),(1,1,1),saturation)
        c1 = make_material('c1',(0.8,0,0),(1,1,1),saturation)
        c2 = make_material('c2',(0.6,0,0),(1,1,1),saturation)
        c3 = make_material('c3',(0.4,0,0.2),(1,1,1),saturation)
        c4 = make_material('c4',(0.2,0,0.4),(1,1,1),saturation)
        c5 = make_material('c5',(0,0,0.6),(1,1,1),saturation)
        c6 = make_material('c6',(0,0,0.8),(1,1,1),saturation)
        c7 = make_material('c7',(0,0,1),(1,1,1),saturation)
        c8 = make_material('c8',(0.7,0.7,0.7),(1,1,1),saturation)
        c9 = make_material('c9',(0.5,0.5,0.5),(1,1,1),saturation)

        #Set the background color to black
        bpy.context.scene.world.horizon_color = (0, 0, 0)

        #File where X,Y and Z data of particles will be stored as plain text 
        try:
            path = bpy.data.scenes['Scene'].my_tool.path
            file_with_data_files = open(path, 'r+')
            line = file_with_data_files.readline()
            file_with_data_files.close()
            
            for cnt in range(0,int(line)):
                file_with_particles_data_extra = open(path + '.' + str(cnt) + '.particles_places.txt', 'w')
                #file_with_particles_data_extra = open(path + '.test.particles_places.txt', 'w')

                try:
                    lista = list_with_data(cnt)
                except:
                    bpy.context.window_manager.popup_menu(error_message, title="An error ocurred", icon='CANCEL')


                ob = bpy.ops.mesh.primitive_uv_sphere_add(size=0.2, location=(0,0,0))

                emitter = bpy.context.object

                bpy.ops.object.particle_system_add()    
                psys1 = emitter.particle_systems[0]
                                
                psys1.name = 'Drops'

                num_total_particles = len(lista)

                actual_particle = 0

                particles_number = num_total_particles


                #Sets the configuration for the particle system of each emitter
                configure_particles(psys1)
                nombreMesh = "Figura" + str(cnt)
                me = bpy.data.meshes.new(nombreMesh)
                
                nombreObjeto="Sphere"
                if (cnt>0 and cnt<10):
                    nombreObjeto = "Sphere.00" + str(cnt)
                if (cnt>=10 and cnt<100):
                    nombreObjeto = "Sphere.0" + str(cnt)
                
                ob = bpy.data.objects.get(nombreObjeto, me)
                ob.active_material = make_material('c2',(0.6,0,0),(1,1,1),saturation)
                ob.active_material.diffuse_color = (0.256219, 0.454065, 0.6)
                ob.active_material.alpha = 0.0984277



                #ob = bpy.data.objects.get("Sphere", me)
                #ob.active_material = c9

                #Sets the coulur of the particles of this emitter
                #set_colour(7,me)

                psys1 = emitter.particle_systems[0]  

                #Stores the X,Y and Z values of each particle for each emitter
                for pa in psys1.particles:
                    if (particles_number > 0):
                        xx = (float(lista[actual_particle][0]))
                        yy = (float(lista[actual_particle][1]))
                        zz = (float(lista[actual_particle][2]))

                        particles_number = particles_number - 1
                        actual_particle = actual_particle +1

                        file_with_particles_data_extra.write("{0} {1} {2} \n".format(xx,yy,zz))
     

                file_with_particles_data_extra.close()  
        except:
            bpy.context.window_manager.popup_menu(error_message2, title="An error ocurred", icon='CANCEL')
       
        #Avanzar en la escena para mostrar los cambios al renderizar OBLIGATORIO 
        bpy.context.scene.frame_current = bpy.context.scene.frame_current + 1        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)       
        bpy.ops.particle.stabilizer()          


        #Estabilization of particles to solve the Blender problem wich makes particles flow arround space

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

# ------------------------------------------------------------------------
#    Register and unregister functions
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(ParticlesGenerator)


def unregister():
    bpy.utils.unregister_class(ParticlesGenerator)
    
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()   
