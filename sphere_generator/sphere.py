import math

class generic_sphere:
    """
    This class describes the modeled sphere, either it is in 2 or 3 dimensions,
    """

    def __init__(self, x, y, z, r):
        """Initialization of the sphere and the dimenstions that it exists

        Args:
            xx (float): x coordinate of the center
            yy (float): y coordinate of the center
            zz (float): z coordinate of the center
            rr (float): radius of the sphere
            dimension (int): The dimensions that the sphere exists (2D or 3D space)
        """

        self._x = x
        self._y = y
        self._z = z
        self._r = r
    

    @property
    def x(self):
        return self._x

    
    @property
    def y(self):
        return self._y


    @property
    def z(self):
        if self._z != None:
            return self._z
        else:
            pass
    
    
    @property
    def r(self):
        return self._r

    def volume(self):
        pass


class sphere_2D(generic_sphere):
    def __init__(self, x, y, r):
        super().__init__(x, y, None, r)
    

    def volume(self):
        """calculates the volume of a 2D sphere (disc area) for the current radius

        Returns:
            Disc Area (float): the disc area
        """
        return math.pi*(self.r**2)
    

class sphere_3D(generic_sphere):
    def __init__(self, x, y, z, r):
        super().__init__(x, y, z, r)
           

    def volume(self):
        """calculates the volume of a 2D sphere (disc area) for the current radius

        Returns:
            Disc Area (float): the disc area
        """
        return (4/3)*math.pi*(self.r**3)