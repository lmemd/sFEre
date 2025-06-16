import math
from .shape import Shape

class sphere_2D(Shape):
    def __init__(self,xx,yy,rr):
        super().__init__(xx,yy,0.0)
        self.r = rr

    def __hash__(self)->int:
        return hash((self.dim_x, self.dim_y, self.r))
    
    #overload to know if 2 2D spheres are the same
    def __eq__(self, other)->None:
        if not isinstance(other, sphere_2D): #if object is not sphere_2D don't compare
            return False
        if self.x == other.x and self.y == other.y and self.r == other.r:
            return True
        return False

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

    
class sphere_3D(Shape):
    def __init__(self,xx,yy,zz,rr):
        super().__init__(xx,yy,zz)
        self.r = rr
           
    def __hash__(self)->int:
        return hash((self.x, self.y, self.z, self.r))

   #overload to know if 2 3D spheres are the same 
    def __eq__(self, other)->None:
        if not isinstance(other, sphere_3D):
            return False
        if self.x == other.x and self.y == other.y and self.z == other.z and self.r == other.r:
            return True
        return False
    
    #attribute to be user friendly
    @property
    def volume(self)->float:
        """calculates the volume of a 3D sphere for the current radius

        Returns:
           Sphere Volume (float) : sphere's volume 
        """
        return (4/3)*math.pi*(self.r**3)