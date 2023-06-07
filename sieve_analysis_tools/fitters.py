from reliability.Fitters import Fit_Weibull_Mixture, Fit_Everything, Fit_Normal_2P
from reliability.Other_functions import histogram
import numpy as np
import matplotlib.pyplot as plt
import math
import sieve_analysis_tools.statistical_tools as st
import sieve_analysis_tools.distributions as dist
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

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

def fit_mixed_Gaussian(failures,bin_edges):
    """
    Fits a mixture of two Gaussian distributions to the provided failure data.

    Parameters:
    ----------
    failures : array-like
        The failure data to fit the mixture model to.
    bin_edges : array-like
        The bin edges used for histogramming the failure data.

    Returns:
    -------
    dict
        A dictionary containing the estimated parameters of the mixture model.
        The dictionary keys are as follows:
        - 'mean 1': The mean of the first Gaussian distribution.
        - 'std 1': The standard deviation of the first Gaussian distribution.
        - 'mean 2': The mean of the second Gaussian distribution.
        - 'std 2': The standard deviation of the second Gaussian distribution.
        - 'mix proportion': The mixing proportion of the first Gaussian distribution.

    """
    def bimodal(x,mu1,sigma1,p1, mu2,sigma2, p2):
        """
        Bimodal Gaussian function used for fitting the mixture model.

        Parameters:
        ----------
        x : array-like
            The x-values.
        mu1 : float
            Mean of the first Gaussian distribution.
        sigma1 : float
            Standard deviation of the first Gaussian distribution.
        p1 : float
            Mixing proportion of the first Gaussian distribution.
        mu2 : float
            Mean of the second Gaussian distribution.
        sigma2 : float
            Standard deviation of the second Gaussian distribution.
        p2 : float
            Mixing proportion of the second Gaussian distribution.

        Returns:
        -------
        array-like
            The y-values of the bimodal Gaussian function.
        """  
        
        return p1 * np.exp(-0.5 * ((x - mu1) / sigma1) ** 2) + p2 * np.exp(-0.5 * ((x - mu2) / sigma2) ** 2)
    
    y,x=np.histogram(failures,bins=bin_edges)
    x=(x[1:]+x[:-1])/2 # for len(x)==len(y)
    
    # Estimate initial parameters
    peaks,_ = find_peaks(y)
    mean_estimates = x[peaks][1:][::-1]
    stdev_estimates = np.array([np.std(x)/3, np.std(x)/3])
    amplitude_estimates = y[peaks][1:][::-1]

    # Combine the initial parameter estimates
    expected = [mean_estimates[0], stdev_estimates[0], amplitude_estimates[0], mean_estimates[1], stdev_estimates[1], amplitude_estimates[1]]
    print("estimates: ", expected)
    params,cov=curve_fit(bimodal,x,y,expected)

    scale_factors_sum = params[2] + params[5]
    p1_norm = params[2] / scale_factors_sum
    p2_norm = params[5] / scale_factors_sum
    print(p1_norm,p2_norm)

    results = {'mean 1' : params[0], 'std 1': params[1], 'mean 2': params[3], 'std 2': params[4], 'mix proportion': p1_norm}

    return results

def calculate_size_distribution_params(bin_edges,frequency,distribution):
    """Calculate Gaussian parameters for given bin values and frequency.

    Args:
        bin_edges (numpy.ndarray): An array of bin values.
        frequency (numpy.ndarray): An array of frequencies.
        distribution(string): The distribution to be fitted. Options are "Gaussian", "Mixed Weibull" and "Mixed Gaussian"

    Returns:
        tuple: A tuple with two elements. The first element is an object with Gaussian distribution parameters.
            The second element is an array of all the data used for fitting the distribution.
    """
    bin_values = st.calculate_bin_centers(bin_edges)
    bin_values, frequency = st.sort_data(bin_values, frequency)
    frequency = st.normalize_frequency(frequency)
    all_data = np.array([bin_values[i] for i in range(len(bin_values)) for j in range(int(frequency[i]))])
    
    if distribution == "Gaussian":
        results = fit_Gaussian(all_data)
    elif distribution == "Mixed Weibull":
        results = fit_weibull_mixture(all_data)
    elif distribution == 'Mixed Gaussian':
        results = fit_mixed_Gaussian(all_data,bin_edges)

    return results, all_data

def fit_sieve_distribution(sieve_analysis_data,shot_material_density,fitting_distribution):
    """
    Fits either a normal distribution or a Weibull distribution to the given sieve data.
    
    Args:
    sieve_data (np.ndarray): The data obtained from sieve analysis.

    Returns:
    tuple: A tuple containing the parameters of the fitted distribution. If a normal distribution is fitted, the tuple
        contains (mu, sigma); if a Weibull distribution is fitted, the tuple contains (alpha, beta).
    """
    sieve_levels = sieve_analysis_data[0]
    retained_weight = sieve_analysis_data[1]
    
    bin_edges, weight_per_sieve = st.sort_data(sieve_levels, retained_weight)
    bin_centers = st.calculate_bin_centers(bin_edges)  

    number_of_shots = st.calculate_number_of_shots(bin_centers, weight_per_sieve,shot_material_density)

    # Fit a Gaussian distribution
    if fitting_distribution == "Gaussian":
        
        fitted_gaussian, data = calculate_size_distribution_params(bin_edges,number_of_shots,fitting_distribution)            
        fitted_distribution = dist.GaussianDistribution(fitted_gaussian.mu, fitted_gaussian.sigma)
    
    # Otherwise, fit a Mixed Weibull distribution
    elif fitting_distribution == "Mixed Weibull":       
        
        fitted_mixed_weibull, data = calculate_size_distribution_params( bin_edges, number_of_shots,fitting_distribution)           
        fitted_distribution = dist.MixedWeibull(fitted_mixed_weibull.alpha_1, fitted_mixed_weibull.beta_1, fitted_mixed_weibull.alpha_2, fitted_mixed_weibull.beta_2, fitted_mixed_weibull.proportion_1)
    
    elif fitting_distribution == "Mixed Gaussian":
        fitted_mixed_gaussian, data = calculate_size_distribution_params(bin_edges, number_of_shots,fitting_distribution)
        fitted_distribution = dist.Mixed_Gaussian(fitted_mixed_gaussian['mean 1'], fitted_mixed_gaussian['std 1'], fitted_mixed_gaussian['mean 2'], fitted_mixed_gaussian['std 2'], fitted_mixed_gaussian['mix proportion'])

    print("Size distribution for sieve analysis data: " + fitting_distribution, sep='\n')
    print(fitted_distribution.__dict__)
    return fitted_distribution