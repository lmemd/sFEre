class generic_box:
    """
    This class describes the modelled box, either it is in 2 or 3 dimensions,
    """
    def __init__(self,dim_xx,dim_yy,dim_zz):
        
        self.dim_x = dim_xx
        self.dim_y = dim_yy
        self.dim_z = dim_zz
        
class box_2D(generic_box):

    def __init__(self,dim_xx,dim_yy):
        super().__init__(dim_xx,dim_yy,0)
        
class box_3D(generic_box):
    def __init__(self,dim_xx,dim_yy,dim_zz):
        super().__init__(dim_xx,dim_yy,dim_zz)

