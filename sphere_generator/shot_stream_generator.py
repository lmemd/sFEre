from genericpath import exists
from logging import raiseExceptions
from numpy import cumsum
from .sphere import sphere_2D,sphere_3D
import random
import math
from matplotlib import pyplot as plt
import numpy as np
from sieve_analysis_tools import statistical_tools as st
import sieve_analysis_tools.distributions as dist
import sieve_analysis_tools.statistical_tools as st
from .utilities import impigment_diameter_calculation,covered_area
class shot_stream:
    """A class that describes the shot stream

    Attributes:
       number_of_spheres (int) : The total number of spheres
       problem_dimensions (int) : The dimensions of the current model, either 2 (2D) or 3 (3D)
       domain_dimensions (box) : The box dimensions (width,height,length) in which the stream exists
       impact angle (float) : The angle of the stream in degrees.
       box_offset_dists (tupple) : The distances for the stream to be offseted in space
       mean_radius (float) : The average radius of the shots
       radius_standard_deviation (float) : The standard deviation of the diameter
    """   
    
    number_of_spheres = 1
    problem_dimensions = 0
    domain_dimensions = None
    impact_angle = 0
    box_offset_dists = (0,0,0)
    mean_radius = 0 
    radius_standard_deviation = 0

    def __init__(self, 
                number_of_spheres_setter, 
                problem_dimensions_setter, 
                domain_dimensions_setter,
                impact_angle_setter,
                box_offset_dists_setter=(0,0,0),     
                mean_radius_setter=mean_radius,
                radius_standard_deviation_setter=radius_standard_deviation, 
                ):


        """Initialize attributes with given values
        """
        self.problem_dimensions = problem_dimensions_setter
        self.domain_dimensions = domain_dimensions_setter
        self.impact_angle = impact_angle_setter
        self.box_offset_dists = box_offset_dists_setter
        
        if isinstance(mean_radius_setter, list):
            self.mean_radius = mean_radius_setter
        else:
            self.mean_radius = [mean_radius_setter]

        if isinstance(radius_standard_deviation_setter, list):
            self.radius_standard_deviation = radius_standard_deviation_setter
        else:
            self.radius_standard_deviation = [radius_standard_deviation_setter]
        
        if isinstance(number_of_spheres_setter,list):
            self.number_of_spheres = number_of_spheres_setter
        else:
            self.number_of_spheres = [number_of_spheres_setter]


    def random_sphere_inside_box(self,r):
        """Creates a sphere, random positioned INSIDE the given box using a uniform distribution. Specifically the WHOLE sphere must lies 
       inside the box. The box may be inclined, in a specified angle. The center of the bottom surface of
       the box is on (0,0,0), although it may be moved, according to specified offset distances. This 
       function works for 2D and 3D spheres.

        Args:
            r (float): The radius of the desired sphere

        Returns:
            sphere: The created sphere
        """

        offset_x = self.box_offset_dists[0]
        offset_y = self.box_offset_dists[1]
        offset_z = self.box_offset_dists[2]
        box = self.domain_dimensions

        y = random.uniform(r, box.dim_y-r)  + offset_y    
           
        #check if the box is vertical (impact angle other than 90 degrees)
        if abs(self.impact_angle - 90) <= 0.00001:         
            x = random.uniform(-box.dim_x/2 + r , box.dim_x/2 - r) + offset_x     
        else:   
            x = random.uniform(-box.dim_x/2 + r , box.dim_x/2 - r)  + y/math.tan(self.impact_angle*math.pi/180) + offset_x

        if box.dim_z == 0:    
            return sphere_2D(x,y,r)    
        else:
            z = random.uniform(-box.dim_z/2 + r , box.dim_z/2 - r) + offset_z
            return sphere_3D(x,y,z,r)

    def single_sphere(position, radius):
        """Creates a single sphere, given the position and radius.

        Args:
            position (list or tuple): A list, which contains the coordinates 
            of sphere's center.
            radius (float): Sphere's radius.

        Returns:
            list: List which contains only a sphere.
        """
        
        if len(position) == 2:
            return [sphere_2D(position[0], position[1], radius)]
        else:
            return [sphere_3D(position[0], position[1], position[2], radius)]

    def structured_spheres(position_list, radius_list):
        """Creates spheres with a structured way, 
        given the positions and radiuses of spheres.

        Args:
            position (list or tuple): A list which, contains tuples or lists
            with the center of each sphere.
            radius (float): A list or tuple, which contains the radius of each 
            sphere.

        Returns:
            list: List of spheres.
        """
        spheres = []
        if len(position_list[0]) == 2:
            for position, radius in zip(position_list, radius_list):
                spheres.append(sphere_2D(position[0], position[1], radius))
        else:
            for position, radius in zip(position_list, radius_list):
                spheres.append(sphere_3D(position[0], position[1], position[2], radius))

        return spheres

    def generate(self):
        """Generates a shot stream according to the given attributes. The spheres are not allowed to intersect.

            Returns:
                list: A list of spheres

            Raises:
                AssertionError: If the lengths of `mean_radius`, `radius_standard_deviation`, and `number_of_spheres`
                                do not match.

            Notes:
                The method generates spheres for each combination of mean radius, standard deviation, and number of spheres
                specified in the respective attributes. The spheres are randomly created and allocated in space, following
                the specified distribution parameters. The method checks for intersections with previously generated spheres
                to ensure non-intersecting spheres are added to the shot stream. The process continues until the requested
                number of spheres for each combination is achieved or the maximum number of loop iterations is reached.

                The lengths of `mean_radius`, `radius_standard_deviation`, and `number_of_spheres` must match, indicating the
                number of combinations to generate.

                If the requested number of spheres cannot be achieved due to intersections, a warning message is printed,
                and the actual number of created spheres is returned.

        """
        no_sphere_loops = 0 #total number of loops for each distribution. If they exceed a limit, the loop stops
        spheres = []        
        #Loop for each shot
        #####################################################
        for m,std,no in zip(self.mean_radius,self.radius_standard_deviation,self.number_of_spheres):
            spheres_counter = 0
            while spheres_counter < no and no_sphere_loops <= 2e3:
                
                #create and allocate the sphere in space
                #####################################################
                
                r = random.gauss(m,std)
                s = self.random_sphere_inside_box(r)
                
                ######################################################
                #spheres.append(s)
                
                #check if size criteria are satisfied
                intersection = self.intersects_existing(s,spheres)
                if not intersection:
                    spheres_counter += 1
                    spheres.append(s) #add the created sphere to the list
                    no_sphere_loops = 0 #zero-out the sphere loops iterator
                else:
                    no_sphere_loops += 1

        if sum(self.number_of_spheres) > len(spheres):
                print("Requested number of spheres could not be achieved due to intersections, a total of " + str(len(spheres)) + " created instead.")
        
        return spheres

    def intersects_existing(self,sph,spheres):
        """This function checks for intersection between the created spheres. Any new created sphere
       is checked for any existing.

        Args:
            sph (sphere): Current sphere
            spheres (list): A list with created spheres

        Returns:
            boolean: True or False, if the sphere intersects existing spheres or not
        """
     
        for s in spheres:
            dist = math.sqrt((sph.x-s.x)**2 + (sph.y-s.y)**2 + (sph.z-s.z)**2)
            if dist < s.r + sph.r:
                return True

        return False

    def plot_coverage(self,spheres,nominal_velocity=None):
        """Plots the spot marks of the shot impact, in the area of interest. Only works for vertical shot stream.
           The radius of each spot mark is calculated as the 34% of the sphere diameter. For example a sphere with
           a diameter of 1.2 mm, will leave a spot mark with radius 0.41 mm.

        Args:
            spheres (list): The spheres list of the shot stream
        """
        box = self.domain_dimensions

        plt.figure()
        if box.dim_z != 0:
            shots = []  
            for sph in spheres:
                
                dent = impigment_diameter_calculation(sph.r,nominal_velocity) 
                
                circle = plt.Circle((sph.x, sph.z), dent/2 , edgecolor = 'black', facecolor = 'red', alpha = 0.08)
                plt.gca().add_patch(circle)
                shots.append((sph.x, sph.z, dent/2))
            plt.gca().set_xlim((-box.dim_x/2, box.dim_x/2))
            plt.gca().set_ylim((-box.dim_z/2, box.dim_z/2))
            
            plt.gca().set_aspect('equal','box')

            plt.gca().grid()
            
            plt.title("Coverage")


        elif box.dim_z == 0:
            print('Coverage plot is only available in 3D spheres')
            return
        

    def plot_spheres(self,spheres):
        """Plots the generated spheres, in space or in plane.

        Args:
            spheres (list): The spheres list of the shot stream
        """
        
        box = self.domain_dimensions
        
        x_centers = np.empty((0,), dtype=float)
        y_centers = np.empty((0,), dtype=float)
        z_centers = np.empty((0,), dtype=float)
        radii = np.empty((0,), dtype=float)
        
        for sph in spheres:
            
            x_centers = np.append(x_centers, sph.x)
            y_centers = np.append(y_centers, sph.y)
            z_centers = np.append(z_centers, sph.z)
            radii = np.append(radii, sph.r)

        if box.dim_z != 0:

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Plot each sphere
            for x_center, y_center, z_center, radius in zip(x_centers, y_centers, z_centers, radii):
                u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
                x = x_center + radius*np.cos(u)*np.sin(v)
                y = y_center + radius*np.sin(u)*np.sin(v)
                z = z_center + radius*np.cos(v)
                ax.plot_wireframe(x, y, z, color='b')

            # Set the limits of each axis to be equal and set the aspect ratio
            ax.set_xlim(-box.dim_x/2, box.dim_x/2)
            ax.set_ylim(0, box.dim_y)
            ax.set_zlim(-box.dim_z/2, box.dim_z/2)
            ax.set_box_aspect((1,1,1))  # set the aspect ratio to be equal
            
            # Set axis labels and display plot
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            

        elif box.dim_z == 0:
            for x_center, y_center, radius in zip(x_centers, y_centers,radii):
                circle = plt.Circle((x_center, y_center), radius , edgecolor = 'black', facecolor = 'red', alpha = 0.3)
            
                plt.gca().set_xlim((-box.dim_x/2, box.dim_x/2))
                plt.gca().set_ylim((0, box.dim_y))

                plt.gca().add_patch(circle)
                
                plt.gca().set_aspect('equal')

                plt.gca().grid()
            

    def calculate_density_of_spheres(self,list_of_spheres):
        """Calculates the ratio of the occupied by spheres volume. 
           The ratio: Total spheres volume/Total space(box) volume

        Args:
            list_of_spheres (list): the list of created spheres

        Returns:
            float: The volume ratio
        """

        box = self.domain_dimensions

        total_volume = sum([s.volume() for s in list_of_spheres])        

        if box.dim_z == 0:    
            return total_volume/(box.dim_x*box.dim_y)  
        else:
            return total_volume/(box.dim_x*box.dim_y*box.dim_z)

    def calculate_coverage(self,circle_centers,shots_dents,resolution):
        """
        Calculate the coverage percentage of a rectangular surface given the circle centers and dent radii of shots.

        Parameters:
            circle_centers (list): List of (x, y) coordinates representing the centers of the circles.
            shots_dents (list): List of dent (impigment) radii corresponding to each circle.
            resolution (float): Grid resolution for dividing the surface.

        Returns:
            list: List of percentages representing the coverage of the rectangular surface for each threshold value.

        Note:
            The function assumes that the rectangular surface dimensions are provided by the `self.domain_dimensions` attribute.
           
        """
        
        box = self.domain_dimensions

        return covered_area(circle_centers,shots_dents, box.dim_x - 2*self.mean_radius[0], box.dim_z - 2*self.mean_radius[0],resolution)


































