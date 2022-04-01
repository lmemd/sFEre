import math

class generic_sphere:
    """
    This class describes a generic sphere embedded in a n-dimensional space
    """

    def __init__(self, ndim = 3, center = [0,0,0], r = 0):
        """Initialization of the sphere and the dimensions that it exists

        Args:
            x (float): x coordinate of the center
            y (float): y coordinate of the center
            z (float): z coordinate of the center
            r (float): radius of the sphere
        """

        self.ndim   = ndim
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
            

class sphere_2D(generic_sphere): #TODO refactor all code referencing it and delete
    def __init__(self,x,y,radius):
        super().__init__(ndim = 2, center = (x,y), r = radius)
    
class sphere_3D(generic_sphere): #TODO refactor all code referencing it and delete
    def __init__(self,x,y,z,radius):
        super().__init__(ndim = 3, center = (x,y,z), r = radius)