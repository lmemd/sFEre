from sphere_generator.sphere import sphere_3D
from sphere_generator.shot_stream_generator import shot_stream
from FE_mesh.configure_shots_mesh import mesh_interface
import os 

def main():

    radius = 0.5 # average radius of created sphere

    # Define sphere's position in space
    x, y, z = 0, 0, 0

    # Define FE length for spheres
    element_length = 0.04

    # Define sphere's filename
    filename = "single_sphere_spherified"
    #define the directory
    parent_dir = os.getcwd()
    directory = parent_dir + '/generated_spheres/' #the directory for the final output

    # Define FE mesh and spacing method
    sphere = shot_stream.single_sphere([x, y, z], radius)
    mesh_interface("spherified_cube", "nonlinear", sphere, element_length, filename, directory, output_option = "LSDYNA") # process and output of meshed generated spheres

    #Plot is not available for structured batches or single sphere

if __name__ == "__main__":
    main()
