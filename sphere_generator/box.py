class generic_box:
    """
    This class describes a generic box embedded in a n-dimensional space.
    """
    #TODO modify so that the box can have arbitrary size, position and orientation
    def __init__(self,ndim = 3, sides = (0,0,0)):
        self.ndim   = ndim
        self.sides  = sides

    @property
    def dim_x(self):
        return self.sides[0]
    
    @property
    def dim_y(self):
        return self.sides[1]

    @property
    def dim_x(self):
        return self.sides[2]
        
class box_2D(generic_box): #TODO refactor all code referencing it and delete
    def __init__(self,dim_x,dim_y):
        super().__init__(ndim=2, sides=(dim_x,dim_y))
        
class box_3D(generic_box): #TODO refactor all code referencing it and delete
    def __init__(self,dim_x,dim_y,dim_z):
        super().__init__(ndim=3, sides=(dim_x,dim_y,dim_z))

