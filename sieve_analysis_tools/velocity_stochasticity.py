import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import sieve_analysis_tools.distributions as dist

def normally_distributed_velocity(nominal_velocity, standard_deviation, lower_cuttof = 0, upper_cutoff = np.inf):
    """
    Generate a normally distributed velocity value based on a given nominal velocity and standard deviation,
    subject to specified lower and upper limits.

    Parameters:
    -----------
    nominal_velocity: float
        The nominal velocity of the shot or shot stream. This is the mean value of the generated velocities.
    standard_deviation: float
        The standard deviation of the generated velocities. This determines how spread out the velocities are
        around the nominal velocity.
    lower_cutoff: float (optional)
        The lower limit for the generated velocity. Default value = 0
    upper_cutoff: float (optional)
        The upper limit for the generated velocity. Default value = inf. 

    Returns:
    --------
    float
        A random velocity value that follows a normal distribution with mean equal to the nominal velocity and 
        standard deviation equal to the given standard deviation.
    """
    
    normalized_std = standard_deviation/nominal_velocity
    normal_distribution = dist.GaussianDistribution(1,normalized_std)
    
    velocity = normal_distribution.generate_random_numbers(1)*nominal_velocity
    
    while not lower_cuttof < velocity and not velocity < upper_cutoff:
        velocity = normal_distribution.generate_random_numbers(1)*nominal_velocity
    
    return velocity

def mixed_velocities(nominal_velocity, percentage_of_retainment, 
                          mean_reduced, std_reduced, reduced_value_range, retained_proportional_factor ):
    pass

def mixed_random_velocities(mean, std, lower_cutoff, upper_cutoff, lower_range, upper_range, gaussian_weight = 0.5):
    pass





def print_tuple(*init_velocity_args):
    """
    Print each item in a tuple.

    Parameters:
    -----------
    *args : tuple
        A tuple with an unknown number of items.
    """
    print(init_velocity_args[0])
    for item in init_velocity_args:
        print(item)





