from FE_mesh.configure_shots_mesh import *
from FE_mesh.LSDYNA_keyword_manager import apply_initial_velocity
from FE_mesh.ABAQUS_keyword_manager import creat_abq_set
from sphere_generator.shot_stream_generator import shot_stream
from sphere_generator.utilities import *
import os
from sieve_analysis_tools import sieve_analysis_evaluation as s

def main():
    #**************************************INPUT SECTION******************************************
    filename_to_export = "S330_75_batch_no_int_No" # name of sphere file
    mean_radius = 1./2 # average radius of created sphere
    radius_std = 0.135/2 # standard deviation of radius for the created sphere
    spheres_number = 55 # total number of sphere created
    spheres_batches = 1 # change this variable if you want to create more than one batch of shots

    # Define FE length for spheres
    element_length = 0.04

    #Define material and properties for FE solver
    PID = 100000
    MID = 100000
    solver = 'LSDYNA'

    # Initial velocity applied m/s and velocity configuration
    velocity = 75 
    velocity_standard_deviation = 0
    maximum_velocity = velocity
    minimum_velocity = 75

    # Define the domain characteristics (the space that contains the created spheres)
    box_width = 2.5 # width of the domain containing the spheres (alongside X axis)
    box_length = 2.5 # length of the domain containing the spheres (alongside Z axis)
    box_height = 15. # height of the domain containing the spheres (alongside Y axis)
    box_angle = 90 # change this value if you want an inlcined box (defined by the angle between the box and the XZ plane)

    parent_dir = os.getcwd()
    directory = parent_dir + '/generated_spheres/' #the directory for the final output


    # Define if your problem is in 2 dimensional or 3 dimensional space (2D or 3D)
    # If the problem is 2D, only length and height of the box are taken into account

    #****************FE sphere mesh is not implemented if problem is 2D****************

    problem_dimensions = problem_dimensions_setter("3D") # Input 2D or 3D according to your problem dimensions
    box = box_getter(problem_dimensions,box_width,box_height,box_length) # create the box 

    #***********************************END OF INPUT SECTION**************************************

    spheres_list, coverage_list, velocities_list = [], [], [] # initialize empty spheres list

    for set_number in range(spheres_batches):

        # Generate stream of random distributed shots in space
        stream = shot_stream(spheres_number, 
                            problem_dimensions, 
                            box, 
                            box_angle, 
                            mean_radius_setter=mean_radius,
                            radius_standard_deviation_setter=radius_std)
        
        #Set the intersection_flag to True, if you don't want any intersections between spheres
        spheres = stream.generate(intersection_flag=True) # Create the stream
        spheres_list.extend(spheres)
        
        # Change the filename according to current index of set number
        filename = f"{filename_to_export}{set_number + 1}"
        
        # Define FE mesh and spacing method
        # process and output of meshed generated spheres
        (nodes, elements) = create_mesh_geometry("spherified_cube", "nonlinear", spheres, element_length, directory, renumbering_point=10000000)

        #Output the entities in selected solver format
        export_mesh_geometry(nodes, elements, filename, solver, PID, MID) #if you don't want to output geometry to a file, comment this
        
        # Call this function if you want to apply initial velocity to the shot stream, in LSDYNA keyword format.
        applied_velocity = apply_initial_velocity(filename, "Constant", 
                                                  *(velocity, velocity_standard_deviation, minimum_velocity, maximum_velocity), 
                                                  angle = box_angle, dyna_id=PID)
        
        velocities_list.append(applied_velocity)


        #Calculate percentage of coverage
        shot_dents_radii = [impigment_diameter_calculation(sph.r,velocity)/2 for sph in spheres_list]
        centers = [(sph.x , sph.z) for sph in spheres_list]
        coverage = stream.calculate_coverage(centers,shot_dents_radii,0.01)
        coverage_list.append(coverage)

    
    # Create Plots
    '''
    plt.figure("Coverage List") 
    transposed_data = np.transpose(coverage_list)
    plt.xlabel("Threshold")
    plt.ylabel("Percentage of points above the threshold")
    for i, item_group in enumerate(transposed_data):
        plt.plot(i+1, item_group, "ob", label='Item {}'.format(i + 1))
    plt.legend()
    '''
    plt.figure("Coverage") 
    transposed_data = np.transpose(coverage_list)
    plt.xlabel("Threshold")
    plt.ylabel("Percentage of points above the threshold")
    for i, item_group in enumerate(transposed_data):
        plt.bar(i, item_group, width = 0.8, color = 'blue')
    plt.xticks(range(len(transposed_data)), labels = ['{} Spheres'.format(i+1) for i in range(len(transposed_data))])
    


    #Plot covered area
    stream.plot_coverage(spheres_list,velocity)

    #Plot velocity distributions
    visualize_velocity_distribution(velocities_list)    
        
    # 3D plot of generated spheres        
    stream.plot_spheres(spheres_list)

    #if you want to try the new plot3d with huge rendering difference for big numbers of spheres
    # new way of plotting 3D spheres, DOESN'T WORK!!!!
    #stream.plot_spheres_v2(spheres_list, color=(0, 0, 255))
    
    
    
    # Print the X,Y coordinates and the radii of created spheres
    list_to_print = ['%.4f'%s.x + '    ' +  '%.4f'%s.y + '   ' +  '%.4f'%s.z + '    ' +  '%.4f'%s.r for s in spheres]
    list_to_print.insert(0,'X coord    Y coord    Z coord    Radius')
    print(*list_to_print, sep='\n')

    # Show Plots
    plt.show()

if __name__ == "__main__":
    main()

