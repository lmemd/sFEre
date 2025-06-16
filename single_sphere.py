from sphere_generator.sphere import sphere_3D
from sphere_generator.shot_stream_generator import shot_stream
from FE_mesh.configure_shots_mesh import *
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
    (nodes, elements) = create_mesh_geometry("spherified_cube", "nonlinear", sphere, element_length, directory) # process and output of meshed generated spheres
    export_mesh_geometry(nodes, elements, filename, "LSDYNA", pid = 1000000) #if you don't want to output geometry to a file, comment this

    #Plot is not available for structured batches or single sphere

if __name__ == "__main__":
    main()
