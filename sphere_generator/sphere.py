import math

class Sphere:
    """
    This class describes the modeled sphere, either it is in 2 or 3 dimensions,
    """
    def __init__(self,xx = 0.0, yy = 0.0, zz = 0.0, rr = 0.0):
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
    
    @property
    def volume(self)->None:
        pass

class sphere_2D(Sphere):

    def __init__(self,xx,yy,rr):
        super().__init__(xx,yy,0,rr)
    
    #using private _area function to give the user context about what volume returns for 2D spheres
    def _area(self)->float:
        return math.pi * self.r ** 2
    
    #attribute to be user friendly
    @property
    def volume(self)->float:
        """calculates the volume of a 2D sphere (disc area) for the current radius

        Returns:
            Disc Area (float): the disc area
        """
        return self._area()
    
class sphere_3D(Sphere):
    def __init__(self,xx,yy,zz,rr):
        super().__init__(xx,yy,zz,rr)
           
    #attribute to be user friendly
    @property
    def volume(self)->float:
        """calculates the volume of a 2D sphere (disc area) for the current radius

        Returns:
            Disc Area (float): the disc area
        """
        return (4/3)*math.pi*(self.r**3)