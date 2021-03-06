from genericpath import exists
from logging import raiseExceptions
from numpy import cumsum
from .sphere import sphere_2D,sphere_3D
import random
import math
from matplotlib import pyplot as plt
import numpy as np

class shot_stream:
    """A class that describes the shot stream

    Attributes:
       number_of_spheres (int) : The total number of spheres
       problem_dimensions (int) : The dimensions of the current model, either 2 (2D) or 3 (3D)
       domain_dimensions (box) : The box dimensions (width,height,length) in which the stream exists
       impact angle (float) : The angle of the stream in degrees.
       box_offset_dists (tupple) : The distances for the stream to be offseted in space
       mean_diameter (float) : The average diameter of the shots
       diameter_standard_deviation (float) : The standard deviation of the diameter
    """
    
    number_of_spheres = 1
    problem_dimensions = 0
    domain_dimensions = None
    impact_angle = 0
    box_offset_dists = (0,0,0)
    mean_diameter = 0 
    diameter_standard_deviation = 0

    def __init__(self,number_of_spheres_setter,problem_dimensions_setter,domain_dimensions_setter,impact_angle_setter, mean_diameter_setter, diameter_standard_deviation_setter,box_offset_dists_setter=(0,0,0)):
        """Initialize attributes with given values
        """
        self.number_of_spheres = number_of_spheres_setter
        self.problem_dimensions = problem_dimensions_setter
        self.domain_dimensions = domain_dimensions_setter
        self.impact_angle = impact_angle_setter
        self.box_offset_dists = box_offset_dists_setter
        self.mean_diameter = mean_diameter_setter
        self.diameter_standard_deviation = diameter_standard_deviation_setter
        
    
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
        """Generates a shot stream, according to given attributes. The spheres are not intersecting.

        Returns:
            list: A list of spheres
        """
        no_sphere_loops = 0 #total number of loops for each distribution. If they exceed a limit, the loop stops
        spheres = []
        
        #Loop for each shot
        #####################################################
        while len(spheres) < self.number_of_spheres and no_sphere_loops <= 2e2:
            
            #create and allocate the sphere in space
            #####################################################
            r = random.gauss(self.mean_diameter,self.diameter_standard_deviation)          
            s = self.random_sphere_inside_box(r)
            ######################################################

            #check if size criteria are satisfied
            if not s.r < 0.1 and not s.r > 2 and not s.y < s.r + 0.01 and not self.intersects_existing(s,spheres):
                spheres.append(s) #add the created sphere to the list
                no_sphere_loops = 0 #zero-out the sphere loops iterator

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
            if dist <= s.r + sph.r:
                return True
        return False

    def plot_coverage(self,spheres):
        """Plots the spot marks of the shot impact, in the area of interest. Only works for vertical shot stream.
           The radius of each spot mark is calculated as the 34% of the sphere diameter. For example a sphere with
           a diameter of 1.2 mm, will leave a spot mark with radius 0.41 mm.

        Args:
            spheres (list): The spheres list of the shot stream
        """
        box = self.domain_dimensions
        if box.dim_z != 0:

            for sph in spheres:
                dent = 2*sph.r*(0.4/1.18)

                circle = plt.Circle((sph.x, sph.z), dent/2 , edgecolor = 'black', facecolor = 'red', alpha = 0.08)
                plt.gca().add_patch(circle)

            plt.gca().set_xlim((-box.dim_x/2, box.dim_x/2))
            plt.gca().set_ylim((-box.dim_z/2, box.dim_z/2))
            
            plt.gca().set_aspect('equal','box')

            plt.gca().grid()
            
            plt.title("Coverage")
            plt.show()
        
        elif box.dim_z == 0:
            print('Coverage plot is only available in 3D spheres')
            return
    
    def plot_spheres(self,spheres):
        """Plots the generated spheres, in space or in plane.
           WARNING: Definitely needs optimization

        Args:
            spheres (list): The spheres list of the shot stream
        """
        
        box = self.domain_dimensions
        points = np.empty((0,3), int)
        radii  = np.empty((0,1), int)

        for sph in spheres:
            
            points = np.append(points, np.array([[sph.x,sph.y,sph.z]]), axis=0)
            radii = np.append(radii, np.array([[sph.r]]), axis=0)

        if box.dim_z != 0:

            def disks2(disk, radius):
                """Creates the 2D disk in parametric form, to be used in 3D sphere plotting.

                Args:
                    disk (list): The list with x,y,z coordinates
                    radius (float): The radius of the sphere

                Returns:
                    float: the x,y,z coordinates of the sphere in space
                """
                u = np.linspace(0, 2 * np.pi, 100)
                v = np.linspace(0, np.pi, 100)
                x = radius * np.outer(np.cos(u), np.sin(v))
                y = radius * np.outer(np.sin(u), np.sin(v))
                z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
                
                return x+disk[0],y+disk[1],z+disk[2]

            def plotting_spheres(data,box_dimensions):
                """Main plotter of the 3D sphere

                Args:
                    data (list): The list with the x,z,y and u,v parameters
                    box_dimensions (tuple): The dimensions of the 3D space
                """
                fig = plt.figure(figsize=(12,12), dpi=300)
                ax = fig.add_subplot(111, projection='3d')
                for k,sph in enumerate(data):
                    x, y, z = sph[0], sph[1], sph[2]
                    ax.plot_surface(x, y, z,  rstride=4, cstride=4, 
                                    color = 'blue', linewidth=0, alpha=0.5)

                ax.set_box_aspect(aspect = box_dimensions)
                plt.show()
            
            data = [disks2(points[k,:], radii[k]) for k in range(self.number_of_spheres)]
            plotting_spheres(data,(box.dim_x,box.dim_y,box.dim_z))

        elif box.dim_z == 0:
            for coord,radius in zip(points,radii):
                circle = plt.Circle((coord[0], coord[1]), radius , edgecolor = 'black', facecolor = 'red', alpha = 0.3)
            
                plt.gca().set_xlim((-box.dim_x/2, box.dim_x/2))
                plt.gca().set_ylim((0, box.dim_y))

                plt.gca().add_patch(circle)
                
                plt.gca().set_aspect('equal')

                plt.gca().grid()
            plt.show()

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

