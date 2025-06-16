from FE_mesh.configure_shots_mesh import mesh_interface
from sphere_generator.shot_stream_generator import shot_stream
from sphere_generator.utilities import *
import os


def main():
    #**************************************INPUT SECTION******************************************
    filename = "structured_spheres" # name of sphere file

    #define the coordinates of spheres in space
    coordinates = [[0, 0, 2] ,\
                   [0, 2, 0], \
                   [2, 0, 0] ]
    
    #define the radius for each sphere
    radii = [1, 1, 1]

    # Define FE length for spheres
    element_length = 0.04

    #define the directory
    parent_dir = os.getcwd()
    directory = parent_dir + '/generated_spheres/' #the directory for the final output

    spheres = shot_stream.structured_spheres(coordinates,radii)
    mesh_interface("spherified_cube", "nonlinear", spheres, element_length, filename, directory,output_option = "LSDYNA") # process and output of meshed generated spheres

    # Print the X,Y coordinates and the radii of created spheres
    list_to_print = ['%.4f'%s.x + '    ' +  '%.4f'%s.y + '   ' +  '%.4f'%s.z + '    ' +  '%.4f'%s.r for s in spheres]
    list_to_print.insert(0,'X coord    Y coord    Z coord    Radius')
    print(*list_to_print, sep='\n')

    #Plot is not available for structured batches or single sphere

if __name__ == "__main__":
    main()

