from reliability.Other_functions import histogram
import numpy as np
import matplotlib.pyplot as plt
import sieve_analysis_tools.statistical_tools as st
#import statistical_tools as st

def sieve_analysis(generated_spheres, measured_weight, inverse_sieve_sizes, rho):
    """
    Perform sieve analysis for spherical particles with given diameters and density, and return
    the retained weight and number of particles on each sieve specified by the given sizes.

    Parameters:
    ----------
    generated_spheres : list
        List of generated sphere diameters in millimeters.
    measured_weight : list
        List of measured weights on each sieve in grams.
    inverse_sieve_sizes : list
        List of inverse sieve sizes in millimeters.
    rho : float
        Density of the material of the particles in grams per cubic centimeter.

    Returns:
    -------
    Nothing
    """

    # Reverse the inverse sieve sizes
    inverse_sieve_sizes = np.array(inverse_sieve_sizes)[::-1]

    # Plot the histogram of generated spheres and calculate the number of shots per sieve
    x, sieve_levels = np.histogram(generated_spheres, inverse_sieve_sizes)
    number_of_shots_per_sieve = np.insert(x, 3, 0)

    # Calculate the sieve centers
    sieve_centers = st.calculate_bin_centers(sieve_levels)

    # Calculate the retained mass for each sieve based on the generated spheres
    generated_retained_mass = []
    for b, i in zip(sieve_centers, x):
        generated_retained_mass.append(i * rho * (4 / 3) * np.pi * (b / 2) ** 3 / 1000)

    # Normalize the generated retained mass and measured weight
    generated_retained_mass_final = st.normalize_frequency(np.insert(generated_retained_mass, -1, 0))
    measured_weight_final = st.normalize_frequency(measured_weight[::-1])

    # Calculate cumulative frequencies of the generated retained mass and measured weight
    cumulative_generated_retained_mass = st.calculate_cumulative_frequencies(generated_retained_mass_final)
    cumulative_measured_weight = st.calculate_cumulative_frequencies(measured_weight_final)

    # Plot the results
    #plt.figure(1)
    #plt.plot(sieve_levels, number_of_shots_per_sieve)
    #plt.gca().invert_xaxis()

    plt.figure()
    plt.plot(sieve_levels, generated_retained_mass_final, 'o-', color='tab:red')
    plt.plot(sieve_levels, measured_weight_final, 'o-', color='tab:blue')

    plt.plot(sieve_levels, cumulative_generated_retained_mass, 'o--', color='tab:red')
    plt.plot(sieve_levels, cumulative_measured_weight, 'o--', color='tab:blue')

    plt.xticks(sieve_levels)
    plt.gca().invert_xaxis()
    plt.title('Cumulative and Normalized Retained weights')
    plt.xlabel('Sieve size (mm)')
    plt.ylabel('Weight (%)')
    plt.grid()
    
