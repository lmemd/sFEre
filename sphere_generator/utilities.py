from .box import box_2D,box_3D
import numpy as np
from matplotlib import pyplot as plt

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
    
def impigment_diameter_calculation(radius,velocity=None):
    """
    Calculate the diameter of an impigment (dent) on a surface caused by an object.

    Parameters:
        radius (float): Radius of the object.
        velocity (float, optional): Velocity of the object.

    Returns:
        float: Diameter of the impigment (dent).
    """
    if isinstance(velocity, float) or isinstance(velocity, int):
        rho = 0.00000000783 #tonne/mm^3 density of steel, only for steel shots
        P = 0.2 # Coefficient of energy loss by the impact
        HB = 509 #N/mm^3 Brinell hardness of the shots, in MPa
        D = 2*radius #diameter of the sphere
        v = velocity*1000 #convert velocity from m/s to mm/s
       
        return 1.278 * D * (P**0.25) * (rho**0.25) * (v**0.5) / (HB**0.25)
    
    else: 
        #approximation that is independent of velocity. Applied only to steel shots, for velocites ranged between 40 and 80 m/s
        return 0.41 * 2 * radius

    
def covered_area(circle_centers,dents_radii,surface_width, surface_height,resolution):

    """
    Calculate the percentage of the points in the covered area of a surface.

    Parameters:
        circle_centers (list): List of (x, y) coordinates representing the centers of the circles.
        dents_radii (list): List of dent (impigment) radii corresponding to each circle.
        surface_dimensions (float): Dimensions of the surface.
        resolution (float): Grid resolution for dividing the surface.

    Returns:
        list: List of percentages representing the coverage of the surface for each threshold value.
    """
    grid_size_width = int(surface_width / resolution)
    grid_size_height = int(surface_height / resolution)
    grid_points_width = np.linspace(-surface_width/2, surface_width/2, grid_size_width)
    grid_points_height = np.linspace(-surface_height/2, surface_height/2, grid_size_height)

    # Create the grid and the 2D array
    X, Y = np.meshgrid(grid_points_width, grid_points_height)
    grid_array = np.zeros((grid_size_height, grid_size_width))

    # Iterate over each grid point
    for i in range(grid_size_height):
        for j in range(grid_size_width):
            x = X[i, j]
            y = Y[i, j]
            
            # Check if the point lies within any of the circles
            for k, center in enumerate(circle_centers):
                radius = dents_radii[k]
                if np.sqrt((x - center[0])**2 + (y - center[1])**2) <= radius:
                    grid_array[i, j] += 1

    thresholds = [ 1, 2, 3, 4, 5, 6]  # Threshold values

    percentage_values = []  # List to store the percentages

    # Iterate over each threshold
    for threshold in thresholds:
        count = np.count_nonzero(grid_array >= threshold)  # Count the points above the threshold
        percentage = count / grid_array.size * 100  # Calculate the percentage
        percentage_values.append(percentage)  # Add the percentage to the list

    # Print the percentages
    for i, threshold in enumerate(thresholds):
        print(f"Percentage of points over {threshold}: {percentage_values[i]:.2f}%")
    
    return percentage_values
    #plt.imshow(grid_array, cmap='hot', origin='lower')
    # Add colorbar
    #plt.colorbar()

