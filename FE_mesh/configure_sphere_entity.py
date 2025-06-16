import time
import numpy as np
import sys 
sys.path.append('../sFEre')

from FE_mesh.sphere_mesh import element_length_translator, create_elements, spacing, renumbering_element_pairs
from FE_mesh.LSDYNA_keyword_manager import output_keyword_file


def mesh_configuration(mesh_method, spacing_method, radius, element_length):
    """Configuration for sphere's mesh.

    Args:
        mesh_method (string): Mesh method to be applied(spherified or normalized).
        spacing_method (string): Spacing method to be applied(linear or nonlinear).
        radius (float): Desired sphere's radius.
        element_length (float): Desired sphere's element length.

    Returns:
        list: List with mesh configurations.
    """
    correction_factor = {"spherified_cube": 0.707543222, "normalized_cube": 1, "spherified_cube_alt": 0.707543222, "normalized_cube_alt": 1}
    correction_factor = correction_factor[mesh_method]

    configs = list(element_length_translator(spacing_method, correction_factor, radius, element_length))
    configs.append(mesh_method)
    configs.append(spacing_method)
    configs = tuple(configs)

    return configs


def sphere_matrices(method, half_length, no_of_elements, scale_factor, transverse_no_of_elements, spacing_method, spacing_factor, position_x, position_y, position_z):
    """Creation of sphere entity, with respect in user's 
    inputs.

    Args:
        method (string): Mesh method (spherified, normalized).
        half_length (float): Described before.
        no_of_elements (float): Described before.
        scale_factor (float): Described before.
        transverse_no_of_elements (float): Described before.
        spacing_method ([type]): Described before.
        spacing_factor (float): Described before.
        position_x (float): Sphere's center x coordinate.
        position_y (float): Sphere's center y coordinate.
        position_z (float): Sphere's center z coordinate.
        pid (int): Described before.

    Returns:
        ndarray: Nodes matrix (LS - DYNA form).
        ndarray: Elements matrix (LS - DYNA form).
    """
    nodes_s = spacing(method, half_length, no_of_elements, scale_factor, transverse_no_of_elements, spacing_method, spacing_factor)
    
    #offset coordinates as user wants, difference of user's center from (0, 0, 0)
    offset_x = position_x - 0
    offset_y = position_y - 0
    offset_z = position_z - 0
    nodes_s[:, 0] = nodes_s[:, 0] + offset_x
    nodes_s[:, 1] = nodes_s[:, 1] + offset_y
    nodes_s[:, 2] = nodes_s[:, 2] + offset_z

    elements_s = create_elements(no_of_elements, transverse_no_of_elements)
    

    # indexing nodes and elements matrices
    # and transform them to the final LS - DYNA form
    index_elements = np.arange(1, np.shape(elements_s)[0] + 1, 1)
    index_nodes = np.arange(1, np.shape(nodes_s)[0] + 1, 1)
    elements_s = np.hstack((np.reshape(index_elements, (np.shape(elements_s)[0], 1)), elements_s))
    nodes_s = np.hstack((np.reshape(index_nodes, (np.shape(nodes_s)[0], 1)), nodes_s))

    # pid number needed for elements matrix formation
    #ones2 = pid * np.ones((np.shape(elements_s)[0], 1))
    #ones2 = np.reshape(ones2, (np.shape(ones2)[0], 1))
    #elements_s = np.hstack((np.reshape(elements_s[:, 0], (np.shape(elements_s)[0], 1)), ones2,
    #                        elements_s[:, 1:]))

    # renumbering elements indices cause python indexing starts from zero
    # but we want them to start from one
    elements_s[:, 1:] += 1

    # deleting unnecessary nodes from model
    index_in = np.unique(elements_s[:, 1:])
    index_out = nodes_s[:, 0]
    index_in = np.flatnonzero(np.invert(np.isin(index_out, index_in)))
    nodes_s = np.delete(nodes_s, index_in, 0)

    # renumbering nodes to exclude ids of the deleted ones
    old_nodes_id = np.copy(nodes_s[:, 0]).astype(int)
    elements_s = elements_s.astype(int)
    #renumbered_id = np.array(list(renumber_nodes_id(old_nodes_id)))
    renumbered_id = np.linspace(1, np.shape(old_nodes_id)[0], num=np.shape(old_nodes_id)[0])
    nodes_s[:, 0] = renumbered_id.astype(int)

    elements_s[:, 1:] = renumbering_element_pairs(old_nodes_id, renumbered_id, elements_s[:, 1:])
    elements_s = np.hstack((elements_s[:, 0:1], elements_s[:, 1:]))
    
    #print("Deleted nodes: %i" %int(np.shape(index_in)[0]))

    return nodes_s, elements_s


def sphere_entity(mesh_method, spacing_method, radius, element_length, position_x, position_y, position_z):
    """Function which creates a sphere entiity, containing 
    nodes and elements matrices.

    Args:
        mesh_method (string): Mesh method to be applied(spherified or normalized).
        spacing_method (string): Spacing method to be applied(linear or nonlinear).
        radius (float): Radius of the sphere.
        element_length (float): Mesh element length.
        position_x (float): Sphere's center x coordinate.
        position_y (float): Sphere's center y coordinate.
        position_z (float): Sphere's center z coordinate.
        pid (int): Described before.

    Returns:
        list: A list, which contains both nodes and 
        elements matrices of the created sphere entity.
    """
    configs = mesh_configuration(mesh_method, spacing_method, radius, element_length)

    half_length = configs[0]
    inner_elements = configs[1]
    scale_factor = configs[2]
    layer_elements = configs[3]
    real_element_length = configs[4]
    spacing_factor = configs[5]
    mesh_method = configs[6]
    spacing_method = configs[7]

    sphere_entity = sphere_matrices(mesh_method, half_length, inner_elements, scale_factor, layer_elements, spacing_method, spacing_factor, position_x, position_y, position_z)

    print('\x1b[1;37;45m' + "Element length (approximately): %f mm. ***" %real_element_length + '\x1b[0m')

    return sphere_entity


"""def main():
    start = time.time()

    shots_name = "sphere_ent"
    radius = 0.4
    element_length = 0.03
    position_x = 0
    position_y = 0
    position_z = 0
    pid = 1000000
    velocity = 100
    angle = 90

    sphere = sphere_entity(radius, element_length, position_x, position_y, position_z, pid)
    nodes_s = sphere[0]
    elements_s = sphere[1]

    renumbering_rule = 10000000

    nodes_s[:, 0] += renumbering_rule
    elements_s[:, 0] += renumbering_rule
    elements_s[:, 2:] += renumbering_rule

    output_keyword_file(nodes_s, elements_s, shots_name, pid, velocity, angle)

    end = time.time()

    print('\x1b[1;37;45m' + "*** Execution time: %f seconds. ***" %(end - start) + '\x1b[0m')


if __name__ == "__main__":
    main()"""
