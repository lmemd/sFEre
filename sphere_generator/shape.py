class Shape:
    '''Class that describes a generic shape in space
    Interface class to use for any other shape that you want to create'''

    def __init__(self, dim_x = 0.0, dim_y = 0.0, dim_z = 0.0):
        self._dim_x = dim_x
        self._dim_y = dim_y
        self._dim_z = dim_z

    #setter/getter methods for compatibility with existing code that uses Box
    @property
    def dim_x(self):
        return self._dim_x
    
    @dim_x.setter
    def dim_x(self, dim_x):
        self._dim_x = dim_x

    @property
    def dim_y(self):
        return self._dim_y
    
    @dim_x.setter
    def dim_y(self, dim_y):
        self._dim_y = dim_y

    @property
    def dim_z(self):
        return self._dim_z
    
    @dim_x.setter
    def dim_z(self, dim_z):
        self._dim_z = dim_z
    
    #setter/getter methods for compatibility with existing code that uses Sphere
    @property
    def x(self):
        return self._dim_x
    
    @x.setter
    def x(self, x):
        self._dim_x = x

    @property
    def y(self):
        return self._dim_y
    
    @y.setter
    def y(self, y):
        self._dim_y = y

    @property
    def z(self):
        return self._dim_z
    
    @z.setter
    def z(self, z):
        self._dim_z = z
    
    @property
    def volume(self):
        pass