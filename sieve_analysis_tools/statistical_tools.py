from reliability.Fitters import Fit_Weibull_Mixture, Fit_Everything, Fit_Normal_2P
from reliability.Other_functions import histogram
import numpy as np
import matplotlib.pyplot as plt
import math

#import distributions as dist

def sort_data(bin_values, frequency):
    """
    Sorts the bin values and corresponding frequencies in ascending order based on bin values.
    
    Args:
    bin_values (list[float]): The diameters of the spheres.
    frequency (list[float]): The frequency of each diameter value.

    Returns:
    tuple[np.ndarray, np.ndarray]: A tuple containing two numpy arrays.
    The first array contains the sorted bin values.
    The second array contains the sorted frequencies.
    """

    sorting_indices = np.argsort(bin_values)
    bin_values = np.array(bin_values)[sorting_indices]
    frequency = np.array(frequency)[sorting_indices]
    return bin_values, frequency

def calculate_cumulative_frequencies(frequencies):
    """Calculate the cumulative frequencies for a sample.

    Args:
        frequencies (list or numpy.ndarray): A list or numpy array of frequencies for a sample.

    Returns:
        numpy.ndarray: A numpy array of cumulative frequencies.
    """
    # Convert input to numpy array for easier manipulation
    frequencies = np.array(frequencies)

    # Calculate cumulative sum of frequencies
    cumulative_frequencies = np.cumsum(frequencies)

    return cumulative_frequencies

def calculate_bin_centers(bin_edges):
    """
    Calculates the bin centers from the bin edges.
    
    Args:
    bin_edges (np.ndarray): The edges of the bins.

    Returns:
    np.ndarray: An array of bin centers.
    """
    return (bin_edges[:-1] + bin_edges[1:]) / 2

def calculate_number_of_shots(bin_centers,mass,density_of_shots):
    """
    Calculates the number of shots for each bin center based on the density of shots.
    
    Args:
    bin_centers (np.ndarray): The centers of the bins.
    mass (np.array): The retained weight per sieve
    density_of_shots (float): The density of shots.

    Returns:
    np.ndarray: An array of number of shots for each bin center.
    """
    average_mass_per_shot = (4/3)*math.pi*((bin_centers/2)**3)*density_of_shots
    return np.around(mass[:-1]/average_mass_per_shot,decimals=0)

def normalize_frequency(frequency):
    """
    Normalizes the frequency by dividing each frequency value by the total sum of frequencies and multiplying by 100.
    
    Args:
    frequency (np.ndarray): The frequency of each bin.

    Returns:
    np.ndarray: An array of normalized frequencies.
    """
    return np.array(frequency) / np.sum(frequency) * 100

def fit_weibull_mixture(failures):
    """
    Fits a Weibull mixture distribution to the data.
    
    Args:
    failures (np.ndarray): The failure data.

    Returns:
    Fit_Weibull_Mixture: The results of the Weibull mixture fit.
    """
    results = Fit_Weibull_Mixture(failures=failures,show_probability_plot=False,print_results=False)
    return results

def fit_Gaussian(failures):
    """
    Fits a Gaussian distribution to the data.
    
    Args:
    failures (np.ndarray): The failure data.

    Returns:
    Fit_Normal_2P: The results of the Weibull mixture fit.
    """
    results = Fit_Normal_2P(failures=failures,show_probability_plot=False,print_results=False)
    return results  


def visualize_histogram(generated_data,bin_edges,data, results):
    """Visualize a histogram with generated data, bin edges, data, and results.

    Args:
        generated_data (numpy.ndarray): An array of generated data to plot.
        bin_edges (numpy.ndarray): An array of bin edges for the histogram.
        data (numpy.ndarray): An array of data to plot on the histogram.
        results (object): An object with distribution data to plot.

    Returns:
        None
    """
    plt.figure(figsize=(9, 5))
    plt.subplot(121)
    histogram(data,bins = bin_edges)
    histogram(generated_data,bins=bin_edges,color="red",alpha=0.3)
    results.distribution.PDF()
    plt.subplot(122)
    histogram(data,bins = bin_edges, cumulative=True)
    histogram(generated_data, bins=bin_edges,cumulative=True,color="red",alpha=0.3)
    results.distribution.CDF()
    plt.show()

def calculate_Weibull_parameters(bin_values, frequency):
    """Calculate Weibull parameters for given bin values and frequency.

    Args:
        bin_values (numpy.ndarray): An array of bin values.
        frequency (numpy.ndarray): An array of frequencies.

    Returns:
        tuple: A tuple with two elements. The first element is an object with Weibull distribution parameters.
            The second element is an array of all the data used for fitting the distribution.
    """
    bin_values_sorted, frequency_sorted = sort_data(bin_values, frequency)
    frequency = normalize_frequency(frequency_sorted)
    all_data = np.array([bin_values_sorted[i] for i in range(len(bin_values_sorted)) for j in range(int(frequency_sorted[i]))])
    results = fit_weibull_mixture(all_data)
    
    return results, all_data

def calculate_Gaussian_parameters(bin_values, frequency):
    """Calculate Gaussian parameters for given bin values and frequency.

    Args:
        bin_values (numpy.ndarray): An array of bin values.
        frequency (numpy.ndarray): An array of frequencies.

    Returns:
        tuple: A tuple with two elements. The first element is an object with Gaussian distribution parameters.
            The second element is an array of all the data used for fitting the distribution.
    """
    bin_values, frequency = sort_data(bin_values, frequency)
    frequency = normalize_frequency(frequency)
    all_data = np.array([bin_values[i] for i in range(len(bin_values)) for j in range(int(frequency[i]))])
    results = fit_Gaussian(all_data)
    
    return results, all_data

#Debuggin code
'''
def generate_sphere_from_sieve_analysis_data(sieves,retained_weight,distribution_fitting_method,shots_material_density,no_of_shots=1):
    
    bin_edges, weight_per_sieve = sort_data(sieves, retained_weight)
    bin_centers = calculate_bin_centers(bin_edges)
    number_of_shots = calculate_number_of_shots(bin_centers, weight_per_sieve,shots_material_density)

    #print(bin_centers,number_of_shots)

    if distribution_fitting_method == "Gaussian" or distribution_fitting_method == "Normal":

        fitted_gaussian, data = calculate_Gaussian_parameters(bin_edges[:-1],number_of_shots)
        fitted_distribution = dist.GaussianDistribution(fitted_gaussian.mu, fitted_gaussian.sigma)
        generated_data =fitted_distribution.generate_random_numbers(no_of_shots)

        return generated_data

    elif distribution_fitting_method == "Mixed Weibull":
        fitted_mixed_weibull, data = calculate_Weibull_parameters(bin_edges[:-1],number_of_shots)
        
        fitted_distribution = dist.MixedWeibull(fitted_mixed_weibull.alpha_1, fitted_mixed_weibull.beta_1, fitted_mixed_weibull.alpha_2, fitted_mixed_weibull.beta_2, fitted_mixed_weibull.proportion_1)
        generated_data = fitted_distribution.generate_random_numbers(no_of_shots)

        
        return generated_data
'''