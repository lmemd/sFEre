import numpy as np

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
        self.apha_1 = alpha_1
        self.beta_1 = beta_1
        self.apha_2 = alpha_2
        self.beta_2 = beta_2
        self.mix_proportion = mix_proportion

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