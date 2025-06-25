import numpy as np
import sys 
import sphere_generator
from FE_mesh.configure_sphere_entity import sphere_entity
from FE_mesh.LSDYNA_keyword_manager import output_keyword_file, output_general_file
from FE_mesh.ABAQUS_keyword_manager import output_inp_file_entities
from FE_mesh.utilities import working_directory

#call this if you want the mesh to be exported to a file
def export_mesh_geometry(nodes, elements, filename, output_option, pid, mid):
    """Export mesh geometry to a file.

    Args:
        nodes (numpy.ndarray): Nodes array.
        elements (numpy.ndarray): Elements array.
        filename (str): Output filename.
        pid (int): Property ID
        mid (int): Material ID
    """
    if output_option == "general":
        output_general_file(nodes, elements, filename)
    elif output_option == "LSDYNA":
        output_keyword_file(nodes, elements, pid, mid, filename)
    elif output_option == "LSDYNA-entities":
        output_keyword_file(nodes, elements, pid, mid, filename, apply_property=False)
    elif output_option == "ABAQUS":
        output_inp_file_entities(nodes, elements, pid, mid, filename)
    else:
        print("Please choose a valid output option: general, LSDYNA or LSDYNA-entities.")

def create_mesh_geometry(mesh_method, spacing_method, spheres, element_length, output_path, renumbering_point = 0):
    """
    Generates a mesh for multiple spheres using specified mesh and spacing methods.

    Args:
        mesh_method (str): Method ("spherified" or "normalized") for FE mesh.
        spacing_method (str): Spacing method ("linear" or "nonlinear") for FE mesh.
        spheres (list): List of initialized sphere objects.
        element_length (float): Desired element length.
        output_path (str): Directory for output.
        renumbering_point (int): Starting index for renumbering mesh entities.

    Returns:
        tuple: (nodes_array, elements_array) containing node and element data.
    """
    
    working_directory(output_path)

    if not isinstance(spheres, list):
        spheres = [spheres]
    
    if any(isinstance(s, sphere_generator.sphere.sphere_2D) for s in spheres):
        print('Mesh generation is not available for 2D spheres')
        return None, None

    nodes_all = np.reshape(np.zeros((1, 4)), (1, 4))
    elements_all = np.reshape(np.zeros((1, 9)), (1, 9))

    for s in spheres:
        [nodes_s_tmp, elements_s_tmp] = sphere_entity(mesh_method, spacing_method, s.r, element_length, s.x, s.y, s.z)

        # renumber indexes of elements and nodes ids
        nodes_s_tmp[:, 0] += np.shape(nodes_all)[0] - 1 # here we dont need + 1 
        # because we have added a row of zeros to be able to call vstack
        elements_s_tmp[:, 0] += np.shape(elements_all)[0] - 1
        elements_s_tmp[:, 1:] += np.shape(nodes_all)[0] - 1

        # appending nodes and elements matrices
        nodes_all = np.vstack((nodes_all, nodes_s_tmp))
        elements_all = np.vstack((elements_all, elements_s_tmp))

    # deleting useless first row of matrices
    nodes_all = np.delete(nodes_all, 0, 0)
    elements_all = np.delete(elements_all, 0, 0)
    
    nodes_all[:, 0] += renumbering_point
    elements_all[:, 0] += renumbering_point
    elements_all[:, 1:] += renumbering_point

    return (nodes_all, elements_all)

        