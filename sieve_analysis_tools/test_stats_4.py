from reliability.Fitters import Fit_Weibull_Mixture, Fit_Everything, Fit_Normal_2P
from reliability.Distributions import Weibull_Distribution, Mixture_Model
from reliability.Other_functions import histogram
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import weibull_min
import random
import statistical_tools as st

def sieve_analysis(d_list, sieve_sizes, rho,):
    """
    Perform sieve analysis for spherical particles with given diameters and density, and return
    the retained weight and number of particles on each sieve specified by the given sizes.

    Parameters:
    d_list (list): List of particle diameters in millimeters.
    rho (float): Density of the material of the particles in grams per cubic centimeter.
    sieve_sizes (list): List of sieve sizes in millimeters.

    Returns:
    weights (list): List of retained weights on each sieve in grams.
    num_particles (list): List of retained number of particles on each sieve.
    """
    # Calculate the surface area of each sieve in square millimeters
    sieve_areas = [np.pi * (size/2)**2 for size in sieve_sizes]

    # Calculate the volume of each sieve in cubic millimeters
    sieve_volumes = [area * size for area, size in zip(sieve_areas, sieve_sizes)]

    # Calculate the mass of particles that can pass through each sieve in grams
    sieve_masses = [rho * volume / 1000 for volume in sieve_volumes]

    # Calculate the retained weight and number of particles on each sieve
    weights = [0] * len(sieve_sizes)
    num_particles = [0] * len(sieve_sizes)
    for d in d_list:
        for i in range(len(sieve_sizes)):
            if d < sieve_sizes[i]:
                particle_mass = rho * (4/3) * np.pi * (d/2)**3 / 1000
                weights[i] += particle_mass
                num_particles[i] += 1
                break
            elif i == len(sieve_sizes) - 1:
                particle_mass = rho * (4/3) * np.pi * (d/2)**3 / 1000
                weights[i] += particle_mass
                num_particles[i] += 1

    # Return the list of retained weights and number of particles on each sieve
    return weights, num_particles

def plot_sieve_analysis(sieve_sizes, retained_weights, cumulative_weights):
    """
    Plots the retained weights and cumulative weights on each sieve.

    Args:
    - sieve_sizes: a 1D array of desired sieve diameters in mm (float or int).
    - retained_weights: a 1D array of retained weights on each sieve in grams (float).
    - cumulative_weights: a 1D array of cumulative weights on each sieve in grams (float).

    Returns: None
    """
    fig, ax1 = plt.subplots()

    # Plot retained weights
    ax1.set_xlabel('Sieve size (mm)')
    ax1.set_ylabel('Retained weight (g)', color='tab:blue')
    ax1.plot(sieve_sizes, retained_weights, 'o-', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Plot cumulative weights
    ax2 = ax1.twinx()
    ax2.set_ylabel('Cumulative weight (g)', color='tab:red')
    ax2.plot(sieve_sizes, cumulative_weights, 'o-', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Set plot title and display plot
    plt.title('Virtual Sieve Analysis')
    plt.show()

def test():
    bin_values = [2., 1.6, 1.4, 1.25, 1.12, 1., 0.9, 0.8, 0.71, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.]
    frequency = [0.0, 0.1, 2.4, 46.3, 42.4, 24.8, 5.6, 5.3, 5.3, 8.8, 9.7, 7.1, 1.7, 0.2, 0.1, 0.0]
    bin_values, frequency = st.sort_data(bin_values,frequency)
    #print(bin_values,frequency)


    generated,fitted_distribution,data = st.generate_sphere_from_sieve_analysis_data(bin_values,frequency,"Mixed Weibull",0.00785,no_of_shots=1000)
    #print(fitted_distribution)


    st.visualize_histogram(generated,bin_values,data, fitted_distribution)
    
    
    perform_sieve_analysis, number_retained = sieve_analysis(generated, bin_values, 0.00785)
    normalized_generated_retained_weight = st.normalize_frequency(perform_sieve_analysis)
    normalized_measured_retained_weight = st.normalize_frequency(frequency)
    print(number_retained)
    plt.plot(bin_values,normalized_generated_retained_weight)
    plt.plot(bin_values,normalized_measured_retained_weight)
    #print(normalized_retained_weight)
    plt.show()
    
    #print(perform_sieve_analysis[0],perform_sieve_analysis[0])
test()