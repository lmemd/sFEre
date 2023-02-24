import numpy as np

def sieve_analysis(d_list, rho, sieve_sizes):
    """
    Perform sieve analysis for spherical particles with given diameters and density, and return
    the retained weight on each sieve specified by the given sizes.

    Parameters:
    d_list (list): List of particle diameters in millimeters.
    rho (float): Density of the material of the particles in grams per cubic centimeter.
    sieve_sizes (list): List of sieve sizes in millimeters.

    Returns:
    weights (list): List of retained weights on each sieve in grams.
    """
    # Calculate the surface area of each sieve in square millimeters
    sieve_areas = [np.pi * (size/2)**2 for size in sieve_sizes]

    # Calculate the volume of each sieve in cubic millimeters
    sieve_volumes = [area * size for area, size in zip(sieve_areas, sieve_sizes)]

    # Calculate the mass of particles that can pass through each sieve in grams
    sieve_masses = [rho * volume / 1000 for volume in sieve_volumes]

    # Calculate the retained weight on each sieve
    weights = [0] * len(sieve_sizes)
    for d in d_list:
        for i in range(len(sieve_sizes)):
            if d < sieve_sizes[i]:
                weights[i] += rho * (4/3) * np.pi * (d/2)**3 / 1000
                break
            elif i == len(sieve_sizes) - 1:
                weights[i] += rho * (4/3) * np.pi * (d/2)**3 / 1000

    # Return the list of retained weights on each sieve
    return weights

# Example usage
d_list = [1.2, 0.8, 1.5, 0.3, 2.0] # list of particle diameters in millimeters
rho = 2.7 # density of particle material in grams per cubic centimeter
sieve_sizes = [4, 2, 1, 0.5, 0.25] # sieve sizes in millimeters

# Perform sieve analysis
weights = sieve_analysis(d_list, rho, sieve_sizes)

# Print the retained weight on each sieve
print("Sieve size (mm)\tRetained weight (g)")
for i in range(len(sieve_sizes)):
    print("{:.2f}\t\t{:.2f}".format(sieve_sizes[i], weights[i]))
