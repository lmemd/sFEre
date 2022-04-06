'''
1. LS-Dyna functions must be included in separate file
2. Mesh should be a separate class
3. Mesh quality criteria should be created
'''
import numpy as np
import numpy_indexed as npi

from numpy.lib.twodim_base import mask_indices


def grid3d_inner_cube(half_length, no_of_elements):
    """This function, creates the coordinates of inner cube,which 
    will be projected at sphere's surface after to form the mesh.

    Args:
        half_length (float): Inner cube's sides half length.
        Example: for a AxAxA cube, half_length = A/2 etc.

        no_of_elements (float): Half side's elements.
        Example: for a side with B elements, no_of_elements = B/2 etc.

    Returns:
        ndarray: Inner cube's coordinates.
    """
    x = np.linspace(-half_length, half_length, num=int(2 * no_of_elements + 1))
    y = np.copy(x)
    x_line, y_line = np.meshgrid(x, y)

    z_line = np.copy(x)
    z_line = np.tile(z_line, (np.shape(x_line)[0]*np.shape(x_line)[1], 1)).T
    z_line = np.reshape(z_line, (np.shape(z_line)[0] * np.shape(z_line)[1], 1))

    x_line = np.reshape(x_line, (np.shape(x_line)[0] ** 2, 1))
    y_line = np.reshape(y_line, (np.shape(y_line)[0] ** 2, 1))

    x_line = np.tile(x_line, (np.shape(x)[0], 1))
    y_line = np.tile(y_line, (np.shape(y)[0], 1))

    grid_output = np.hstack((x_line, y_line, z_line))

    return grid_output


def element_length_translator(spacing_method, correction_factor, radius, element_length):
    """This function translates user's inputs in order
    for other functions to use them and produce the mesh.

    Args:
        spacing_method (string): The mesh method algorithm (normalized, spherified).
        correction_factor (float): Correction factor to predict  real element length.
        radius (float): Sphere's radius.
        element_length (float): Desired element length to be produced.

    Returns:
        float : Half length.
        float : Cube's elements.
        float : Scale factor to project cube to sphere's surface.
        float : Elements in between cube and sphere's surface.
        float : Real element length (approximately).
        float : Spacing factor for layer elements lengths.
    """
    scale_factor = 3.4142 # this parameter needs tuning

    half_length = radius/scale_factor 

    density = correction_factor*radius/element_length
    if abs(density - np.floor(density)) < 0.25:
        density = int(np.floor(density))

    elif 0.25 <= abs(density - np.floor(density)) < 0.75:
        density = int(np.floor(density)) + 0.5

    elif 0.75 <= abs(density - np.floor(density)):
        density = int(np.ceil(density))

    inner_elements = density # unchanged parameter
    #scale_factor_for_layers = 2 # this parameter needs tuning!
    #layer_elements = scale_factor_for_layers*density
    if spacing_method == "linear":
        layer_elements = int(2*density)

    else:
        add_elements = np.floor(density/2) + 1
        layer_elements = int(density + add_elements)

    spacing_length = (radius - radius/scale_factor)/layer_elements

    real_element_length = correction_factor*radius/inner_elements

    spacing_factor = real_element_length/spacing_length

    return half_length, inner_elements, scale_factor, layer_elements, real_element_length, spacing_factor


def normalized_cube(inner, half_length, scale_factor):
    """Normalized cube algorithm. A cube is projected
    to a sphere's surface and so mesh is produced.
    This algorithm fullfills Jacobian's criteria very nice.

    Args:
        inner (array): Cube's coordinates (produced by another function).
        half_length (float): Cube's side half length.
        scale_factor (float): Scale factor for radius formation.

    Returns:
        float : X axis sphere's coordinates.
        float : Y axis sphere's coordinates.
        float : Z axis sphere's coordinates.
    """
    #Exclude center point(if it exists) cause it produces zero length.
    counter = -1
    center_id = []
    e = 1E-10
    for line in inner:
        counter += 1
        if abs(line[0] - 0) < e and abs(line[1] - 0) < e and abs(line[2] - 0) < e:
            center_id.append(counter)


    inner_copy = np.copy(inner)

    sphere_radius = half_length * scale_factor
    point_length = np.sqrt(inner[:, 0]**2 + inner[:, 1]**2 + inner[:, 2]**2)
    #Transform nodes coordinates, and exclude (0, 0).
    #If number is even, center exists, so exclude it.
    if center_id:
        n = center_id[0]
        inner_copy[0:n, :] = inner_copy[0:n, :]*sphere_radius/np.reshape(point_length[0:n], (np.shape(point_length[0:n])[0], 1))
        inner_copy[n, :] = np.array([0, 0, 0])
        inner_copy[n + 1:, :] = inner_copy[n + 1:, :]*sphere_radius/np.reshape(point_length[n + 1:], (np.shape(point_length[n + 1:])[0], 1))
    #If number is odd, center does not exist, so you don't exclude it.
    else:
        inner_copy = inner_copy*sphere_radius/np.reshape(point_length, (np.shape(point_length)[0], 1))
    
    x = inner_copy[:, 0]
    y = inner_copy[:, 1]
    z = inner_copy[:, 2]

    x = np.reshape(x, (np.shape(x)[0], 1))
    y = np.reshape(y, (np.shape(y)[0], 1))
    z = np.reshape(z, (np.shape(z)[0], 1))

    return x, y, z


def spherified_cube(inner, half_length, scale_factor):
    """Spherified cube algorithm. A cube is projected
    to a sphere's surface and so mesh is produced.
    This algorithm fullfills Jacobian's criteria very nice.

    Args:
        inner (array): Cube's coordinates (produced by another function).
        half_length (float): Cube's side half length.
        scale_factor (float): Scale factor for radius formation.

    Returns:
        float : X axis sphere's coordinates.
        float : Y axis sphere's coordinates.
        float : Z axis sphere's coordinates.
    """
    # outer = inner * scale_factor
    x1 = inner[:, 0] / half_length
    y1 = inner[:, 1] / half_length
    z1 = inner[:, 2] / half_length

    # Transformation of outer coordinates to sphere coordinates
    # Multiplication with scale_factor expands coordinates to catch the final radius
    sphere_radius = half_length * scale_factor
    x = x1 * np.sqrt(1 - y1 ** 2 / 2 - z1 ** 2 / 2 + y1 ** 2 * z1 ** 2 / 3) * sphere_radius
    y = y1 * np.sqrt(1 - z1 ** 2 / 2 - x1 ** 2 / 2 + z1 ** 2 * x1 ** 2 / 3) * sphere_radius
    z = z1 * np.sqrt(1 - x1 ** 2 / 2 - y1 ** 2 / 2 + x1 ** 2 * y1 ** 2 / 3) * sphere_radius

    x = np.reshape(x, (np.shape(x)[0], 1))
    y = np.reshape(y, (np.shape(y)[0], 1))
    z = np.reshape(z, (np.shape(z)[0], 1))
    
    return x, y, z


def spacing_method(method, transverse_no_of_elements, spacing_factor):
    """Spacing algorithm for layer elements between cube and sphere's
    surface.

    Args:
        method (string): Spacing method, linear or not, specifies the way
        of spacing between elements.
        transverse_no_of_elements (float): Elements in between cube and sphere's surface.
        spacing_factor (float): Scale factor for radius formation.

    Returns:
        ndarray: An array which is used to proceed the spacing.
    """
    method_dict = {"linear": 1, "nonlinear": spacing_factor}
    spacing_factor = method_dict[method] # ----> reduce the spacing_factor, reduces spacing of layers
    j = np.linspace(spacing_factor, 1, num=transverse_no_of_elements) # ----> reducing the num of layers, reduces the spacing_factor

    return j


def spacing(method, half_length, no_of_elements, scale_factor, transverse_no_of_elements, spacing_method_input, spacing_factor):
    """Proceeds the spacing between cube and sphere's surface in order
    to have better control and flexibility on mesh accuracy. It can 
    produce linear and non linear spacing, so the user can have better control
    on element's length and shape (Jacobian, aspect ratio etc.).

    Args:
        method (string): Mesh algorithm (spherified or normalized).
        half_length (float): Defined before.
        no_of_elements (float): Defined before.
        scale_factor (float): Defined before.
        transverse_no_of_elements (float): Defined before.
        linear_nonlinear (string): Spacing method (linear or not).
        spacing_factor (float): Defined before.

    Returns:
        ndarray: Returns sphere's mesh coordinates.
    """
    inner = grid3d_inner_cube(half_length, no_of_elements)
    if method == "spherified_cube" or method == "spherified_cube_alt":
        [xx, yy, zz] = spherified_cube(inner, half_length, scale_factor)
    
    elif method == "normalized_cube" or method == "normalized_cube_alt":
        [xx, yy, zz] = normalized_cube(inner, half_length, scale_factor)

    if method == "spherified_cube_alt":
        [xxx, yyy, zzz] = spherified_cube(inner, half_length, half_length)
        inner = np.hstack((xxx, yyy, zzz))
    elif method == "normalized_cube_alt":
        [xxx, yyy, zzz] = normalized_cube(inner, half_length, half_length)
        inner = np.hstack((xxx, yyy, zzz))
    else:
        pass
    
    outer = np.hstack((xx, yy, zz))

    # Spacing of sphere - cube mesh, how many elements, between inner (cube) and outer nodes (sphere)
    spacing_x = (outer[:, 0] - inner[:, 0]) / transverse_no_of_elements
    spacing_y = (outer[:, 1] - inner[:, 1]) / transverse_no_of_elements
    spacing_z = (outer[:, 2] - inner[:, 2]) / transverse_no_of_elements

    spacing_all = np.hstack((np.reshape(spacing_x, (np.shape(spacing_x)[0], 1)),
                             np.reshape(spacing_y, (np.shape(spacing_y)[0], 1)),
                             np.reshape(spacing_z, (np.shape(spacing_z)[0], 1))))

    grid_all = np.zeros((1, np.shape(inner)[1]))

    # Calling spacing method to obtain spacing values for layer elements
    j = spacing_method(spacing_method_input, transverse_no_of_elements, spacing_factor)

    for i in range(transverse_no_of_elements - 1):
        grid_all = np.vstack((grid_all, inner + spacing_all * (i + 1)/j[i]))


    grid_all = np.delete(grid_all, 0, 0)
    grid_all = np.vstack((inner, grid_all, outer))

    return grid_all


def create_elements(no_of_elements, transverse_no_of_elements):
    """This function creates elements matrix (connection matrix),
    which connects the nodes as known from FEM theory.

    Args:
        no_of_elements (float): Defined before.
        transverse_no_of_elements (float): Defined before.

    Returns:
        ndarray: Elements matrix.
    """
    grid1 = int(2 * no_of_elements + 1)
    grid2 = grid1 ** 2
    grid3 = grid1 ** 3

    # 6 sides starting elements
    # we form the inner cube's 6 sides and then we use the algorithm created below
    # to make the elements numbering and creation
    side1 = np.array([[0, 1, 1 + grid2, 0 + grid2]])

    side2 = np.fliplr(np.array([[2 * no_of_elements * grid1, 2 * no_of_elements * grid1 + 1,
    2 * no_of_elements * grid1 + 1 + grid2, 2 * no_of_elements * grid1 + grid2]]))

    side3 = np.array([[2 * no_of_elements, 2 * no_of_elements + grid1,
    2 * no_of_elements + grid1 + grid2, 2 * no_of_elements + grid2]])

    side4 = np.fliplr(np.array([[0, grid1, grid1 + grid2, 0 + grid2]]))
    
    side5 = np.fliplr(np.array([[0, 1, 1 + grid1, 0 + grid1]]))

    side6 = np.array([[(2 * no_of_elements) * grid2, (2 * no_of_elements) * grid2 + 1,
            (2 * no_of_elements) * grid2 + 1 + grid1, (2 * no_of_elements) * grid2 + grid1]])

    # inner cube's starting elements
    # we do the same for the inner cube
    side_cube = np.fliplr(np.copy(side5))

    side1_tmp = np.copy(side1)
    side2_tmp = np.copy(side2)
    side3_tmp = np.copy(side3)
    side4_tmp = np.copy(side4)
    side5_tmp = np.copy(side5)
    side6_tmp = np.copy(side6)
    side_cube_tmp = np.copy(side_cube)

    # loop to form the 1 dimension
    for i in range(int(2 * no_of_elements) - 1):
        side1 = np.vstack((side1, side1_tmp + (i + 1)))
        side2 = np.vstack((side2, side2_tmp + (i + 1)))
        side3 = np.vstack((side3, side3_tmp + (i + 1) * grid1))
        side4 = np.vstack((side4, side4_tmp + (i + 1) * grid1))
        side5 = np.vstack((side5, side5_tmp + (i + 1)))
        side6 = np.vstack((side6, side6_tmp + (i + 1)))
        side_cube = np.vstack((side_cube, side_cube_tmp + (i + 1)))

    side1_tmp = np.copy(side1)
    side2_tmp = np.copy(side2)
    side3_tmp = np.copy(side3)
    side4_tmp = np.copy(side4)
    side5_tmp = np.copy(side5)
    side6_tmp = np.copy(side6)
    side_cube_tmp = np.copy(side_cube)

    # loop to form the 2 dimensions of sides
    for k in range(1, int(2 * no_of_elements)):
        side1 = np.vstack((side1, side1_tmp + k * grid2))
        side2 = np.vstack((side2, side2_tmp + k * grid2))
        side3 = np.vstack((side3, side3_tmp + k * grid2))
        side4 = np.vstack((side4, side4_tmp + k * grid2))
        side5 = np.vstack((side5, side5_tmp + k * grid1))
        side6 = np.vstack((side6, side6_tmp + k * grid1))
        side_cube = np.vstack((side_cube, side_cube_tmp + k * grid1))

    all_sides = np.vstack((side1, side2, side3, side4, side5, side6))

    # loop to form the final 3 dimensional shape
    elements_matrix = np.zeros((1, 8))
    for j in range(transverse_no_of_elements):
        eight_nodes = np.hstack((all_sides + j * (grid3), all_sides + (j + 1) * (grid3)))
        elements_matrix = np.vstack((elements_matrix, eight_nodes))

    # loop to form the final 3 dimensional shape
    # in order to have the potential of a full parametric sphere
    # cube's side can have it's own number of elements, different than the "layer" elements
    for ii in range(int(2*no_of_elements)):
        eight_nodes_cube = np.hstack((side_cube + ii * grid2, side_cube + (ii + 1) * grid2))
        elements_matrix = np.vstack((elements_matrix, eight_nodes_cube))

    elements_matrix = np.delete(elements_matrix, 0, 0)

    return elements_matrix


# amazing way for mapping values of different matrices
def renumbering_element_pairs(old_nodes_id, sorted_nodes_id, elements_matrix):
    """This function, new and old nodes ids, 
    for better matrix handling to avoid big number txt conflicts.

    Args:
        old_nodes_id (array): Nodes before sorting (mapping nodes).
        sorted_nodes_id (array): Nodes after sorting (nodes that will be mapped).
        elements_matrix (array): Elements matrix.

    Returns:
        ndarray : Mapped elements matrix.
    """
    mapping = dict(zip(old_nodes_id, sorted_nodes_id))
    elements_matrix = npi.remap(elements_matrix.flatten(), list(mapping.keys()), list(mapping.values())).reshape(np.shape(elements_matrix)[0], np.shape(elements_matrix)[1])

    return elements_matrix

