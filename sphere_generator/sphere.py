import math

class generic_sphere:
    """
    This class describes a generic sphere embedded in a n-dimensional space
    """

    def __init__(self, center = (0,0,0), r = 0):
        """Initialization of the sphere and the dimensions that it exists
        Args:
            center (array-like): X,Y,Z coordinates of the center respectively
            r (float): radius of the sphere
        """
        self.center = center
        self.r      = r
    
    #TODO eventually delete, only for compatibility
    @property
    def x(self):
        return self.center[0]

    @property
    def y(self):
        return self.center[1]

    @property
    def z(self):
        return self.center[2]
    
    @property
    def ndim(self):
        return len(self.center)
    
    def volume(self):
        """
        Returns the length/area/volume of the 1D/2D/3D sphere.
        """
        if self.ndim == 1: 
            return 2*self.r
        elif self.ndim == 2:
            return math.pi*(self.r**2)
        elif self.ndim == 3:
            return (4/3)*math.pi*(self.r**3)
        else:
            raise ValueError('Volume can only be calculated for 2- or 3- dimensional spheres')
            

class sphere_2D(generic_sphere):
    def __init__(self,center = (0,0), r = 0):
        super().__init__(center, r)
    
class sphere_3D(generic_sphere):
    def __init__(self,center = (0,0,0), r = 0):
        super().__init__(center, r)

#debugging code

sphere = sphere_2D((1,2),3 )
print(sphere.ndim)
print(sphere.r)
print(sphere.x)
print(sphere.volume())

sphere_2 = sphere_3D()
print(sphere_2.volume())