from reliability.Fitters import Fit_Weibull_Mixture, Fit_Everything, Fit_Normal_2P
from reliability.Distributions import Weibull_Distribution, Mixture_Model
from reliability.Other_functions import histogram
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import weibull_min
import random

def sieve_analysis(diameters, sieve_sizes, density):
    """
    Performs virtual sieve analysis on a list of sphere diameters, given the desired sieve sizes and material density.

    Args:
    - diameters: a 1D array of sphere diameters in mm (float or int).
    - sieve_sizes: a 1D array of desired sieve diameters in mm (float or int).
    - density: material density in grams per cubic millimeter (float or int).

    Returns:
    - retained_weights: a 1D array of retained weights on each sieve in grams (float).
    - cumulative_weights: a 1D array of cumulative weights on each sieve in grams (float).
    """

    
    # Sort equivalent diameters in ascending order
    sorted_diameters = np.sort(diameters)
    sieve_sizes = np.sort(sieve_sizes)
    # Calculate the weight of each sphere in grams
    volume = 4/3 * np.pi * (sorted_diameters/2)**3
    mass = volume * density
    
    # Initialize variables to store the weights on each sieve
    retained_weights = np.zeros(len(sieve_sizes))
    cumulative_weights = np.zeros(len(sieve_sizes))
    
    # Perform sieve analysis
    for i in range(len(sieve_sizes)):
        if i == 0:
            retained_weights[i] = np.sum(mass[sorted_diameters <= sieve_sizes[i]])
        elif i == len(sieve_sizes)-1:
            retained_weights[i] = np.sum(mass[sorted_diameters > sieve_sizes[i-1]])
        else:
            retained_weights[i] = np.sum(mass[(sorted_diameters > sieve_sizes[i-1]) & (sorted_diameters <= sieve_sizes[i])])
        
        cumulative_weights[i] = np.sum(retained_weights[:i+1])
    
    return retained_weights, cumulative_weights

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

