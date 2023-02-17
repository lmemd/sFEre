import math

class generic_sphere:
    """
    This class describes the modeled sphere, either it is in 2 or 3 dimensions,
    """
    
    x = 0
    y = 0
    z = 0
    r = 0

    def __init__(self,xx,yy,zz,rr):
        """Initialization of the sphere and the dimenstions that it exists

        Args:
            xx (float): x coordinate of the center
            yy (float): y coordinate of the center
            zz (float): z coordinate of the center
            rr (float): radius of the sphere
            dimension (int): The dimensions that the sphere exists (2D or 3D space)
        """

        self.x = xx
        self.y = yy
        self.z = zz
        self.r = rr
    
    def volume(self):
        pass

class sphere_2D(generic_sphere):

    def __init__(self,xx,yy,rr):
        super().__init__(xx,yy,0,rr)
    
    def volume(self):
        """calculates the volume of a 2D sphere (disc area) for the current radius

        Returns:
            Disc Area (float): the disc area
        """
        return math.pi*(self.r**2)
    
class sphere_3D(generic_sphere):
    def __init__(self,xx,yy,zz,rr):
        super().__init__(xx,yy,zz,rr)
           
    def volume(self):
        """calculates the volume of a 2D sphere (disc area) for the current radius

        Returns:
            Disc Area (float): the disc area
        """
        return (4/3)*math.pi*(self.r**3)