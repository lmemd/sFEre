from FE_mesh.configure_shots_mesh import mesh_interface
from FE_mesh.LSDYNA_keyword_manager import apply_initial_velocity
from sphere_generator.shot_stream_generator import shot_stream
from sphere_generator.utilities import *
import os
from sieve_analysis_tools import sieve_analysis_evaluation as s

def main():
    #**************************************INPUT SECTION******************************************
    filename_to_export = "demo_batch_of_spheres" # name of sphere file
    mean_radius = 0.5 # average radius of created sphere
    radius_std = 0.2 # standard deviation of radius for the created sphere
    spheres_number = 100 # total number of sphere created
    spheres_batches = 1 # change this variable if you want to create more than one batch of shots
    shots_material_density = 0.00785 #in gm/mm^3

    sieve_levels = [2., 1.6, 1.4, 1.25, 1.12, 1., 0.9, 0.8, 0.71, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.]
    retained_weight = [0.0, 0.1, 2.4, 46.3, 42.4, 24.8, 5.6, 5.3, 5.3, 8.8, 9.7, 7.1, 1.7, 0.2, 0.1, 0.0]

    sieve_analysis_data = [sieve_levels , retained_weight]

    # Define FE length for spheres
    element_length = 0.04

    # Define the domain characteristics (the space that contains the created spheres)
    box_width = 2000 # width of the domain containing the spheres (alongside X axis)
    box_length = 2000 # length of the domain containing the spheres (alongside Z axis)
    box_height = 8000 # height of the domain containing the spheres (alongside Y axis)
    box_angle = 90 # change this value if you want an inlcined box (defined by the angle between the box and the XZ plane)

    parent_dir = os.getcwd()
    directory = parent_dir + '/generated_spheres/' #the directory for the final output

    # Define if your problem is in 2 dimensional or 3 dimensional space (2D or 3D)
    # If the problem is 2D, only length and height of the box are taken into account

    #****************FE sphere mesh is not implemented if problem is 2D****************

    problem_dimensions = problem_dimensions_setter("3D") # Input 2D or 3D according to your problem dimensions
    box = box_getter(problem_dimensions,box_width,box_height,box_length) # create the box 

    #***********************************END OF INPUT SECTION**************************************

    spheres_list = [] # initialize empty spheres list
    for set_number in range(spheres_batches):

        # Generate stream of random distributed shots in space
        stream = shot_stream(spheres_number, 
                            problem_dimensions, 
                            box, 
                            box_angle, 
                            sieve_analysis_data_setter=sieve_analysis_data,                             
                            fitting_distribution_setter="Mixed Weibull",
                            material_density_setter=shots_material_density)
        spheres = stream.generate() # Create the stream
        
        # Change the filename according to current index of set number
        filename = f"{filename_to_export}_{set_number + 1}"
        
        # Define FE mesh and spacing method
        # process and output of meshed generated spheres
        #mesh_interface("spherified_cube", "nonlinear", spheres, element_length, filename, directory, "LSDYNA")

        # Call this function if you want to apply initial velocity to the shot stream, in LSDYNA keyword format.
        # Currently, an absolute initial velocity of 70 m/s will be applied.
        #apply_initial_velocity(filename, 70, box_angle)

        spheres_list.extend(spheres)
        print(set_number)
    
    # 3D plot of generated spheres        
    #stream.plot_spheres(spheres_list)
    #stream.plot_coverage(spheres_list)

    generated_diameters = [s.r*2 for s in spheres_list]
    
    s.evaluate(sieve_levels, retained_weight, generated_diameters, shots_material_density)


    # Print the X,Y coordinates and the radii of created spheres
    #list_to_print = ['%.4f'%s.x + '    ' +  '%.4f'%s.y + '   ' +  '%.4f'%s.z + '    ' +  '%.4f'%s.r for s in spheres]
    #list_to_print.insert(0,'X coord    Y coord    Z coord    Radius')
    #print(*list_to_print, sep='\n')

if __name__ == "__main__":
    main()

