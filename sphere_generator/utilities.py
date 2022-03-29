from .box import box_2D,box_3D

def problem_dimensions_setter(dimensions):
    """Sets the problem dimensions, they may be 2 or 3

    Args:
        dimensions (string): The dimensions of the problem. 2D for  two-dimensional problem and 3D for a three-dimensional problem

    Raises:
        Exception: The input strings must be specifically 2D or 3D
        Exception: The input must be a string

    Returns:
        integer: The problem dimensions
    """

    if isinstance(dimensions,str):
        if dimensions == '2D':
            return int(2)
        elif dimensions == '3D':
            return int(3)
        else:
            raise Exception('Please input 2D for a two-dimensional problem and 3D for a three-dimensional problem')
    else:
        raise Exception('Input must be a string')

def box_getter(integer_dimensions, box_width, box_height, box_length = None):
    """Get the box in the specified dimensions

    Args:
        integer_dimensions (int): The dimensions of the problem
        box_width (float): The width of the box, along X axis
        box_height (float): The height of the box along Y axis
        box_length (float): The length of the box along Z axis

    Raises:
        Exception: The input must be an integer

    Returns:
        box: The created box
    """
    if integer_dimensions == 3:
        return box_3D(box_width,box_height,box_length)
    elif integer_dimensions == 2:
        return box_2D(box_width,box_height)
    else:
        raise Exception('Problem dimensions must be integer')