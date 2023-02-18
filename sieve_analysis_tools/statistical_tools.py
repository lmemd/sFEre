from reliability.Fitters import Fit_Weibull_Mixture, Fit_Everything, Fit_Normal_2P
from reliability.Distributions import Weibull_Distribution, Mixture_Model
from reliability.Other_functions import histogram
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import weibull_min
import random

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
    density_of_shots (float): The density of shots.

    Returns:
    np.ndarray: An array of number of shots for each bin center.
    """
    average_mass_per_shot = (4/3)*math.pi*((bin_centers/2)**3)*density_of_shots
    return np.around(mass[1:]/average_mass_per_shot,decimals=0)

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

def generate_mixed_weibull(alpha_1, beta_1, alpha_2, beta_2, mix_proportion, size):
    """
    Generates mixed Weibull data.
    
    Args:
    alpha_1 (float): The shape parameter of the first Weibull distribution.
    beta_1 (float): The scale parameter of the first Weibull distribution.
    alpha_2 (float): The shape parameter of the second Weibull distribution.
    beta_2 (float): The scale parameter of the second Weibull distribution.
    mix_proportion (float): The mixing proportion of the two Weibull distributions.
    size (int): The size of the generated data.

    Returns:
    np.ndarray: An array with the generated data
    """
    weibull_1 = weibull_min(c=beta_1, scale=alpha_1)
    weibull_2 = weibull_min(c=beta_2, scale=alpha_2)

    size_1 = int(size * mix_proportion)
    size_2 = size - size_1

    if size_1 == 0:
        random_numbers_1 = np.array([])
    else:
        random_numbers_1 = weibull_1.rvs(size=size_1)

    if size_2 == 0:
        random_numbers_2 = np.array([])
    else:
        random_numbers_2 = weibull_2.rvs(size=size_2)

    return np.concatenate([random_numbers_1, random_numbers_2])


def generate_gaussian(mu,sigma, size):
    """
    Generates Gaussian distribution datadata.
    
    Args:
    mu (float): The mean value of the Gaussian distribution.
    sigma: The standard deviation of the Gaussian distribution.
    size (int): The size of the generated data.

    Returns:
    np.ndarray: An array with the generated data
    """
    
    data = []
    for i in range(size):
        data.append(random.gauss(mu,sigma))
    
    return np.array(data)

def visualize_histogram(generated_data,bin_edges,data, results):
    
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
    bin_values_sorted, frequency_sorted = sort_data(bin_values, frequency)
    frequency = normalize_frequency(frequency_sorted)
    all_data = np.array([bin_values_sorted[i] for i in range(len(bin_values_sorted)) for j in range(int(frequency_sorted[i]))])
    results = fit_weibull_mixture(all_data)
    
    return results, all_data

def calculate_Gaussian_parameters(bin_values, frequency):
    bin_values, frequency = sort_data(bin_values, frequency)
    frequency = normalize_frequency(frequency)
    all_data = np.array([bin_values[i] for i in range(len(bin_values)) for j in range(int(frequency[i]))])
    results = fit_Gaussian(all_data)
    
    return results, all_data

#Debuggin code


def generate_sphere_from_sieve_analysis_data(sieves,retained_weight,distribution_fitting_method,shots_material_density,no_of_shots=1):
    
    bin_edges, weight_per_sieve = sort_data(sieves, retained_weight)
    bin_centers = calculate_bin_centers(bin_edges)
    number_of_shots = calculate_number_of_shots(bin_centers, weight_per_sieve,shots_material_density)
    #print(number_of_shots)
    if distribution_fitting_method == "Gaussian" or distribution_fitting_method == "Normal":

        fitted_gaussian, data = calculate_Gaussian_parameters(bin_centers, weight_per_sieve)
        mu, sigma = fitted_gaussian.mu, fitted_gaussian.sigma
        generated_data = generate_gaussian(mu,sigma,no_of_shots)

        return generated_data, fitted_gaussian, data

    elif distribution_fitting_method == "Mixed Weibull":
        fitted_mixed_weibull, data = calculate_Weibull_parameters(bin_centers, weight_per_sieve)
        a1, b1, a2, b2, p1, = fitted_mixed_weibull.alpha_1, fitted_mixed_weibull.beta_1, fitted_mixed_weibull.alpha_2, fitted_mixed_weibull.beta_2, fitted_mixed_weibull.proportion_1
        #print(a1,b1,a2,b2,p1)
        generated_data = generate_mixed_weibull(a1, b1, a2, b2, p1, no_of_shots)
        
        return generated_data, fitted_mixed_weibull, data
'''
def test():
    bin_values = [2., 1.6, 1.4, 1.25, 1.12, 1., 0.9, 0.8, 0.71, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.]
    frequency = [0.0, 0.1, 2.4, 46.3, 42.4, 24.8, 5.6, 5.3, 5.3, 8.8, 9.7, 7.1, 1.7, 0.2, 0.1, 0.0]
    bin_values, frequency = sort_data(bin_values,frequency)
    
    generated = []
    for i in range(1):
        generated_data,fitted_distribution,data = generate_sphere_from_sieve_analysis_data(bin_values,frequency,"Mixed Weibull",0.0078,no_of_shots=1)
        generated.extend(generated_data)
        print(generated)

    visualize_histogram(generated,bin_values,data, fitted_distribution)
    print(generated_data)
test()
'''