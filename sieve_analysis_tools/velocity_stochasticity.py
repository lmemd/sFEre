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

def mixed_random_velocities_generator(mean, std, lower_cutoff, upper_cutoff, lower_range, upper_range, gaussian_weight = 0.5):
    '''
    Generates a random number from a mixture of a truncated Gaussian distribution and a uniform distribution with the given mean, standard deviation, range, and cutoff limits. The `gaussian_weight` parameter determines the weight of the Gaussian distribution in the mixture.

    Parameters:
        - mean: Mean of the mixed distribution
        - std: Standard deviation of the mixed distribution
        - lower_cutoff: Lower cutoff limit for the truncated Gaussian distribution
        - upper_cutoff: Upper cutoff limit for the truncated Gaussian distribution
        - lower_range: Lower limit for the uniform distribution
        - upper_range: Upper limit for the uniform distribution
        - gaussian_weight: Weight of the Gaussian distribution in the mixture (default: 0.5)

    Returns:
        A random number from the mixed distribution.
    '''

    # Generate a random number from the truncated Gaussian distribution
    a = (lower_cutoff - mean) / std
    b = (upper_cutoff - mean) / std
    gaussian_num = truncnorm.rvs(a, b, loc=mean, scale=std)
    # Generate a random number from the uniform distribution
    uniform_num = np.random.uniform(low=lower_range, high=upper_range)
    # Calculate the weighted average of the two random numbers
    arr = np.array([gaussian_num, uniform_num])
    weights = np.array([gaussian_weight, 1-gaussian_weight])
    random_num = np.random.choice(arr, p=weights)
    #mixed_num = gaussian_weight*gaussian_num + (1-gaussian_weight)*uniform_num
    return random_num


def mixed_random_velocities(nominal_velocity, retained_initial_velocity, 
                            reduced_velocity, std_reduced, reduced_value_range, percentage_of_retained_velocity):
    
    '''
    Generates a random velocity value for an impact event, based on a given nominal velocity and other parameters. 
    The function uses `mixed_random_velocities_generator` to generate the random velocity value from a mixture of a 
    truncated Gaussian distribution and a uniform distribution.

    Parameters:
        - nominal_velocity: Nominal velocity for the impact event
        - percentage_of_retainment: Percentage of the nominal velocity that is retained after the impact
        - mean_reduced: Mean of the mixed distribution for the reduced velocity
        - std_reduced: Standard deviation of the mixed distribution for the reduced velocity
        - reduced_value_range: Range of values for the reduced velocity
        - retained_proportional_factor: Weight of the reduced velocity in the mixture

    Returns:
        A random velocity value for the impact event.
    '''

    lower_bound_percentage_of_retainement = (100 - retained_initial_velocity)/100
    upper_bound_percentage_of_retainement = 1

    mean_reduced_normalized = reduced_velocity/nominal_velocity
    std_reduced_normalized = std_reduced/nominal_velocity

    lower_value_cutoff = reduced_value_range[0]/nominal_velocity
    upper_value_cutoff = reduced_value_range[1]/nominal_velocity

    velocity = mixed_random_velocities_generator(mean_reduced_normalized, std_reduced_normalized, 
                            lower_value_cutoff, upper_value_cutoff, 
                            lower_bound_percentage_of_retainement, upper_bound_percentage_of_retainement, 
                            percentage_of_retained_velocity/100)
    
    return velocity*nominal_velocity

def visualize_velocity_distribution(velocities):
    '''
    Visualizes the distribution of velocities generated by `mixed_random_velocities` function.

    Parameters:
        - velocities: List of velocity values generated by `mixed_random_velocities` function.

    Returns:
        None.
    '''
    hist, bins = np.histogram(velocities, bins = 10, density=False)

    # Calculate the bin width
    bin_width = bins[1] - bins[0]

    # Convert the counts to percentages
    hist_percent = (hist / float(len(vels))) * 100.0

    # Plot the histogram in percentage
    plt.bar(bins[:-1], hist_percent, width=bin_width, color = "red", alpha = 0.3, edgecolor = "black")
    plt.xlabel('Impact velocities')
    plt.ylabel('Percentage of shots')
    plt.grid()
    plt.show()

def test():
    velocity_params = (70, 10, 70*0.65, 70*0.2, [0.2,1], 0.5)
    number = 20000
    
    vels = []
    for i in range(number):
        vels.append(mixed_random_velocities(*velocity_params))

    visualize_velocity_distribution(vels)

if __name__ == "__main__":
    test()





