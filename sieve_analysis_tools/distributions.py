import numpy as np
from scipy.stats import weibull_min

class GaussianDistribution:
    """
    A class representing a Gaussian distribution with mean and standard deviation attributes.

    Attributes:
    ----------
    mean : float
        The mean of the Gaussian distribution.
    stdev : float
        The standard deviation of the Gaussian distribution.

    Methods:
    -------
    generate_random_numbers(size):
        Generates random numbers from the Gaussian distribution.

    """

    def __init__(self, mean, stdev):
        """
        Initializes a new GaussianDistribution object.

        Parameters:
        ----------
        mean : float
            The mean of the Gaussian distribution.
        stdev : float
            The standard deviation of the Gaussian distribution.
        """
        self.mean = mean
        self.stdev = stdev

    def generate_random_numbers(self, size):
        """
        Generates random numbers from the Gaussian distribution.

        Parameters:
        ----------
        size : int
            The number of random numbers to generate.

        Returns:
        -------
        ndarray
            A numpy array of random numbers drawn from the Gaussian distribution.
        """
        return np.random.normal(self.mean, self.stdev, size)

class MixedWeibull:
    """
    A class representing a Gaussian distribution with mean and standard deviation attributes.

    Attributes:
    ----------
    alpha_1 (float): 
        The shape parameter of the first Weibull distribution.
    beta_1 (float): 
        The scale parameter of the first Weibull distribution.
    alpha_2 (float): 
        The shape parameter of the second Weibull distribution.
    beta_2 (float): 
    
        The scale parameter of the second Weibull distribution.
    mix_proportion (float): 
        The mixing proportion of the two Weibull distributions.

    Methods:
    -------
    generate_random_numbers(size):
        Generates random numbers from the Gaussian distribution.

    """

    def __init__(self, alpha_1, beta_1, alpha_2, beta_2, mix_proportion):
        """
        Initializes a new MixedWeibull object.

        Parameters:
        ----------
        alpha_1 (float): 
            The shape parameter of the first Weibull distribution.
        beta_1 (float): 
            The scale parameter of the first Weibull distribution.
        alpha_2 (float): 
            The shape parameter of the second Weibull distribution.
        beta_2 (float): 
        
            The scale parameter of the second Weibull distribution.
        mix_proportion (float): 
            The mixing proportion of the two Weibull distributions.
        """
        self.alpha_1 = alpha_1
        self.beta_1 = beta_1
        self.alpha_2 = alpha_2
        self.beta_2 = beta_2
        self.mix_proportion = mix_proportion

    def generate_random_numbers(self, size):
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
        weibull_1 = weibull_min(c=self.beta_1, scale=self.alpha_1)
        weibull_2 = weibull_min(c=self.beta_2, scale=self.alpha_2)

        size_1 = int(size * self.mix_proportion)
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
    
class Mixed_Gaussian:
    def __init__(self, mean_1, stdev_1, mean_2, stdev_2, mix_proportion):
        """
        Initializes a new Mixed_Gaussian object.

        Parameters:
        ----------
        mean_1 : float
            The mean of the first Gaussian distribution.
        stdev_1 : float
            The standard deviation of the first Gaussian distribution.
        mean_2 : float
            The mean of the second Gaussian distribution.
        stdev_2 : float
            The standard deviation of the second Gaussian distribution.
        mix_proportion : float
            The proportion of the first Gaussian distribution in the mixture.
        """
        self.mean_1 = mean_1
        self.stdev_1 = stdev_1
        self.mean_2 = mean_2
        self.stdev_2 = stdev_2
        self.mix_proportion = mix_proportion

    def generate_random_numbers(self, size):
        """
        Generates random numbers based on a mixed Gaussian distribution.

        Args:
            num_samples (int): Number of random numbers to generate. Defaults to 1.

        Returns:
            list: A list of randomly generated numbers based on the mixed Gaussian distribution.
        """
        # Calculate the weights for the mixture
        weight_1 = self.mix_proportion
        weight_2 = 1 - self.mix_proportion

        # Generate random numbers based on the mixed Gaussian distribution
        samples = []
        for _ in range(size):
            # Randomly select a Gaussian distribution based on weights
            gaussian_index = np.random.choices([0, 1], weights=[weight_1, weight_2], k=1)[0]

            # Generate a random number from the selected Gaussian distribution
            if gaussian_index == 0:
                mu = self.mean_1
                sigma = self.stdev_1
            else:
                mu = self.mean_2
                sigma = self.stdev_2

            sample = np.random.gauss(mu, sigma)
            samples.append(sample)

        return samples