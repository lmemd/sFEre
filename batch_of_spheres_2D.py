from sphere_generator.shot_stream_generator import shot_stream
from sphere_generator.utilities import *


def main():
    #**************************************INPUT SECTION******************************************
    filename = "demo_batch_of_2D_spheres" # name of sphere file
    mean_radius = 0.5 # average radius of created sphere
    radius_std = 0.2 # standard deviation of radius for the created sphere
    spheres_number = 10 # total number of sphere created
    spheres_batches = 1 # change this variable if you want to create more than one batch of shots

    # Define FE length for spheres
    element_length = 0.04

    # Define the domain characteristics (the space that contains the created spheres)
    box_width = 2 # width of the domain containing the spheres (alongside X axis)
    box_length = 2 # length of the domain containing the spheres (alongside Z axis)
    box_height = 10 # height of the domain containing the spheres (alongside Y axis)
    box_angle = 90 # change this value if you want an inlcined box (defined by the angle between the box and the XZ plane)

    # Define if your problem is in 2 dimensional or 3 dimensional space (2D or 3D)
    # If the problem is 2D, only length and height of the box are taken into account

    #****************FE sphere mesh is not implemented if problem is 2D****************

    problem_dimensions = problem_dimensions_setter("2D") # Input 2D or 3D according to your problem dimensions
    box = box_getter(problem_dimensions,box_width,box_height,box_length) # create the box 

    #***********************************END OF INPUT SECTION**************************************

    spheres_list = [] # initialize empty spheres list, containing all the spheres from every sphere batch

    for set_number in range(spheres_batches):

        # Generate stream of random distributed shots in space
        stream = shot_stream(spheres_number, 
                            problem_dimensions, 
                            box, 
                            box_angle, 
                            mean_radius_setter=mean_radius,
                            radius_standard_deviation_setter=radius_std)
        spheres = stream.generate() # Create the stream
        spheres_list.extend(spheres)
        
        #plot of generated spheres        
        stream.plot_spheres(spheres)
    
    # Print the X,Y coordinates and the radii of created spheres
    list_to_print = ['%.4f'%s.x + '    ' +  '%.4f'%s.y  + '    ' +  '%.4f'%s.r for s in spheres]
    list_to_print.insert(0,'X coord    Y coord    Radius')
    print(*list_to_print, sep='\n')

if __name__ == "__main__":
    main()

