from FE_mesh.configure_shots_mesh import mesh_interface
from FE_mesh.LSDYNA_keyword_manager import apply_initial_velocity
from sphere_generator.shot_stream_generator import shot_stream
from sphere_generator.utilities import *


def main():
    #**************************************INPUT SECTION******************************************
    filename = "demo_batch_of_spheres" # name of sphere file
    mean_radius = 0.5 # average radius of created sphere
    radius_std = 0.2 # standard deviation of radius for the created sphere
    spheres_number = 10 # total number of sphere created
    spheres_batches = 1 # change this variable if you want to create more than one batch of shots

    # Define FE length for spheres
    element_length = 0.04

    # Define the domain characteristics (the space that contains the created spheres)
    box_width = 2 # width of the domain containing the spheres (alongside X axis)
    box_length = 2 # length of the domain containing the spheres (alongside Z axis)
    box_height = 5 # height of the domain containing the spheres (alongside Y axis)
    box_angle = 90 # change this value if you want an inlcined box (defined by the angle between the box and the XZ plane)

    # Define if your problem is in 2 dimensional or 3 dimensional space (2D or 3D)
    # If the problem is 2D, only length and height of the box are taken into account

    #****************FE sphere mesh is not implemented if problem is 2D****************

    problem_dimensions = problem_dimensions_setter("3D") # Input 2D or 3D according to your problem dimensions
    box = box_getter(problem_dimensions,box_width,box_height,box_length) # create the box 

    #***********************************END OF INPUT SECTION**************************************

    spheres_list = [] # initialize empty spheres list
    for set_number in range(spheres_batches):

        # Generate stream of random distributed shots in space
        stream = shot_stream(spheres_number, problem_dimensions, box, box_angle,0.0078, mean_radius, radius_std)
        spheres = stream.generate() # Create the stream
        
        # Change the filename according to current index of set number
        filename = f"{filename}_{set_number + 1}"
        
        # Define FE mesh and spacing method
        # process and output of meshed generated spheres
        mesh_interface("spherified_cube", "nonlinear", spheres, element_length, filename, "LSDYNA")

        # Call this function if you want to apply initial velocity to the shot stream, in LSDYNA keyword format.
        # Currently, an absolute initial velocity of 70 m/s will be applied.
        apply_initial_velocity(filename, 70, box_angle)

        spheres_list.extend(spheres)

        # 3D plot of generated spheres        
        #stream.plot_spheres(spheres_list)
        #stream.plot_coverage(spheres_list)

    # Print the X,Y coordinates and the radii of created spheres
    list_to_print = ['%.4f'%s.x + '    ' +  '%.4f'%s.y + '   ' +  '%.4f'%s.z + '    ' +  '%.4f'%s.r for s in spheres]
    list_to_print.insert(0,'X coord    Y coord    Z coord    Radius')
    print(*list_to_print, sep='\n')

if __name__ == "__main__":
    main()

