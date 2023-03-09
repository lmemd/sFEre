import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import distributions as dist

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
    
    lower_bound_percentage_of_retainement = (100 - percentage_of_retainment)/100
    upper_bound_percentage_of_retainement = 1

    mean_reduced_normalized = mean_reduced/nominal_velocity
    std_reduced_normalized = std_reduced/nominal_velocity

    lower_value_cutoff = reduced_value_range[0]
    upper_value_cutoff = reduced_value_range[1]

    return mean_reduced_normalized, std_reduced_normalized, lower_value_cutoff, upper_value_cutoff, lower_bound_percentage_of_retainement, upper_bound_percentage_of_retainement, retained_proportional_factor

def mixed_random_velocities(mean, std, lower_cutoff, upper_cutoff, lower_range, upper_range, gaussian_weight = 0.5):
    """
    Generates a random number from a mixture of a truncated Gaussian distribution and
    a uniform distribution with the given mean, standard deviation, range, and cutoff limits.
    The `gaussian_weight` parameter determines the weight of the Gaussian distribution
    in the mixture.
    """
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


test = mixed_velocities(70, 10, 70*0.6, 70*0.27, [0.2,1], 0.75)


number = 20000
vels = []
for i in range(number):
    vels.append(mixed_random_velocities(*test))

# Create the histogram
hist, bins = np.histogram(vels, density=False)

# Calculate the bin width
bin_width = bins[1] - bins[0]

# Convert the counts to percentages
hist_percent = (hist / float(len(vels))) * 100.0 * bin_width

# Plot the histogram in percentage
plt.bar(bins[:-1], hist_percent, width=bin_width)
plt.xlabel('Data')
plt.ylabel('Percentage')
plt.show()






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





