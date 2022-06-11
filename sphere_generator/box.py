class generic_box:
    """
    This class describes the modeled sphere, either it is in 2 or 3 dimensions,
    """

    def __init__(self, dim_x = 0, dim_y = 0, dim_z = 0):
        self._dim_x = dim_x
        self._dim_y = dim_y
        self._dim_z = dim_z

    @property
    def dim_x(self):
        return self._dim_x

    
    @property
    def dim_y(self):
        return self._dim_y


    @property
    def dim_z(self):
        if self._dim_z != None:
            return self._dim_z
        else:
            pass
    

class box_2D(generic_box):
    def __init__(self, dim_x = 0, dim_y = 0):
        super().__init__(dim_x, dim_y, None)
        

class box_3D(generic_box):
    def __init__(self, dim_x = 0, dim_y = 0, dim_z = 0):
        super().__init__(dim_x, dim_y, dim_z)