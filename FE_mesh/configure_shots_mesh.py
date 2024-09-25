import numpy as np
import sys 
import sphere_generator
from FE_mesh.configure_sphere_entity import sphere_entity
from FE_mesh.LSDYNA_keyword_manager import output_keyword_file, output_general_file, output_include_file
from FE_mesh.utilities import working_directory

def mesh_interface(mesh_method, spacing_method, spheres, element_length, filename, output_path, output_option, pid = 1, renumbering_point = 0):
    """Generates a batch with multiple spheres, based on given positions,
    radiuses and other characteristics included in the analysis.

    Args:
        mesh_method (string): Method (spherified or normalized) for FE mesh.
        spacing_method (string): Spacing method (linear or nonlinear) for FE mesh.
        spheres (list): List of initialized spheres.
        element_length (float): FE mesh element length.
        filename (str): Name of the batch file.
        output_path (str) : The name of the output path
        pid (int): PID.
        renumbering_point (int): Renumbering point of the .k file entities.
        initial_velocity (boolean or int/float): Initial velocity of generated spheres.

    Returns:
        list: Nodes and elements of sphere mesh.
    """
    working_directory(output_path)
    if not isinstance(spheres, list):
        spheres = [spheres]
    
    if not any(isinstance(s, sphere_generator.sphere.sphere_2D) for s in spheres):

        nodes_all = np.reshape(np.zeros((1, 4)), (1, 4))
        elements_all = np.reshape(np.zeros((1, 10)), (1, 10))
        for s in spheres:
            [nodes_s_tmp, elements_s_tmp] = sphere_entity(mesh_method, spacing_method, s.r, element_length, s.x, s.y, s.z, pid)
            if len(spheres) > 1:
                # renumber indexes of elements and nodes ids
                nodes_s_tmp[:, 0] += np.shape(nodes_all)[0] - 1 # here we dont need + 1 
                # because we have added a row of zeros to be able to call vstack
                elements_s_tmp[:, 0] += np.shape(elements_all)[0] - 1
                elements_s_tmp[:, 2:] += np.shape(nodes_all)[0] - 1

            else:
                pass

            # appending nodes and elements matrices
            nodes_all = np.vstack((nodes_all, nodes_s_tmp))
            elements_all = np.vstack((elements_all, elements_s_tmp))

        # deleting useless first row of matrices
        nodes_all = np.delete(nodes_all, 0, 0)
        elements_all = np.delete(elements_all, 0, 0)
        
        nodes_all[:, 0] += renumbering_point
        elements_all[:, 0] += renumbering_point
        elements_all[:, 2:] += renumbering_point

        if output_option == "general":
            output_general_file(nodes_all, elements_all, filename)
        elif output_option == "LSDYNA":
            output_keyword_file(nodes_all, elements_all, pid, filename)
        elif output_option == "LSDYNA-entities":
            output_include_file(nodes_all, elements_all, pid, filename)
        else:
            print("Nothing was outputed.")

            return nodes_all, elements_all

    else:
        print('Mesh generation is not available for 2D spheres')
        return
        