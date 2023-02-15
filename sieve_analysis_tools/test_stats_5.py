from reliability.Fitters import Fit_Weibull_Mixture, Fit_Everything, Fit_Normal_2P
from reliability.Distributions import Weibull_Distribution, Mixture_Model
from reliability.Other_functions import histogram
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import weibull_min
import random

class DataAnalyzer:
    def __init__(self, bin_values, frequency, density_of_shots):
        self.bin_values = bin_values
        self.frequency = frequency
        self.density_of_shots = density_of_shots
    
    def sort_data(self):
        sorting_indices = np.argsort(self.bin_values)
        self.bin_values = np.array(self.bin_values)[sorting_indices]
        self.frequency = np.array(self.frequency)[sorting_indices]

    def calculate_bin_centers(self):
        self.bin_centers = (self.bin_values[:-1] + self.bin_values[1:]) / 2

    def calculate_number_of_shots(self):
        average_mass_per_shot = (4/3)*math.pi*((self.bin_centers/2)**3)*self.density_of_shots
        self.number_of_shots = np.around(self.mass[:-1]/average_mass_per_shot, decimals=0)

    def normalize_frequency(self):
        self.normalized_frequency = np.array(self.frequency) / np.sum(self.frequency) * 100

    def calculate_mixed_Weibull_parameters(self):
        self.sort_data()
        self.normalize_frequency()
        self.calculate_bin_centers()
        all_data = np.array([self.bin_centers[i] for i in range(len(self.bin_centers)) for j in range(int(self.normalized_frequency[i]))])
        self.results = Fit_Weibull_Mixture(failures=all_data)

        return self.results.alpha_1, self.results.beta_1, self.results.alpha_2, self.results.beta_2, self.results.proportion_1

    def calculate_Gaussian_parameters(self):
        self.sort_data()
        self.normalize_frequency()
        self.calculate_bin_centers()
        all_data = np.array([self.bin_centers[i] for i in range(len(self.bin_centers)) for j in range(int(self.normalized_frequency[i]))])
        self.results = Fit_Normal_2P(failures=all_data)
        
        return self.results.mu, self.results.sigma
   
    def fit_weibull_mixture(self, failures):
        return Fit_Weibull_Mixture(failures=failures)

    def fit_Gaussian(self, failures):
        return Fit_Normal_2P(failures=failures)

    def generate_mixed_weibull(self, alpha_1, beta_1, alpha_2, beta_2, mix_proportion, size):
        weibull_1 = weibull_min(c=beta_1, scale=alpha_1)
        weibull_2 = weibull_min(c=beta_2, scale=alpha_2)

        random_numbers_1 = weibull_1.rvs(size=int(size * mix_proportion))
        random_numbers_2 = weibull_2.rvs(size=int(size * (1 - mix_proportion)))

        return np.concatenate([random_numbers_1, random_numbers_2])

    def generate_gaussian(self, mu, sigma, size):
        data = []
        for i in range(size):
            data.append(random.gauss(mu, sigma))

        return np.array(data)

    def visualize_histogram(self, generated_data, bin_edges, data):
        
        
        plt.figure(figsize=(9, 5))
        plt.subplot(121)
        histogram(data, bins=bin_edges)
        histogram(generated_data, bins=bin_edges, color="red")
        self.results.distribution.PDF()
        plt.subplot(122)
        histogram(data, bins=bin_edges, cumulative=True)
        histogram(generated_data, bins=bin_edges, cumulative=True, color="red")
        self.results.distribution

bin_values = [2., 1.7, 1.18, 1.]
frequency = [0.0, 0.05, 0.8, 0.11]

distr = DataAnalyzer(bin_values,frequency,0.0078)
gaussian_mix = distr.calculate_Gaussian_parameters()
print(gaussian_mix)
generated_data = distr.generate_gaussian(gaussian_mix[0], gaussian_mix[0], 1000)
distr.visualize_histogram(generated_data,bin_values,frequency)
plt.show()