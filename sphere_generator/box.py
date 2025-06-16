class Box:
    """
    This class describes the modelled box, either it is in 2 or 3 dimensions,
    """
    def __init__(self,dim_width = 0.0,dim_height = 0.0,dim_len = 0.0):
        
        self.dim_width = dim_width
        self.dim_height = dim_height
        self.dim_len = dim_len
        
class Box_2D(Box):

    def __init__(self,dim_width = 0.0,dim_height = 0.0):
        super().__init__(dim_width,dim_height,0.0)
        
    @property
    def dim_x(self)->float:
        return self.dim_width
    
    @dim_x.setter
    def dim_x(self, dim_x)->None:
        self.dim_width = dim_x
    
    @property
    def dim_y(self)->float:
        return self.dim_height
    
    @dim_y.setter
    def dim_y(self, dim_y)->None:
        self.dim_height = dim_y

    '''provide a read only dim_z option for compatibility with other .py files
    that use dim_z which now is dim_len
    default .getter'''
    @property
    def dim_z(self):
        return 0 #for a 2D box that is always zero

class Box_3D(Box):
    def __init__(self,dim_width = 0.0,dim_height = 0.0,dim_len = 0.0):
        super().__init__(dim_width,dim_height,dim_len)

    @property
    def dim_x(self)->float:
        return self.dim_width
    
    @dim_x.setter
    def dim_x(self, dim_x)->None:
        self.dim_width = dim_x
    
    @property
    def dim_y(self)->float:
        return self.dim_height
    
    @dim_y.setter
    def dim_y(self, dim_y)->None:
        self.dim_height = dim_y

    @property
    def dim_z(self)->float:
        return self.dim_len
    
    @dim_z.setter
    def dim_z(self, dim_z)->None:
        self.dim_len = dim_z