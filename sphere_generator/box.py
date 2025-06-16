from .shape import Shape

class Box_2D(Shape):

    def __init__(self,dim_width = 0.0,dim_height = 0.0):
        super().__init__(dim_width,dim_height,0.0)

    #define only this to return 0 and not be set for 2D Box     
    @property
    def dim_z(self):
        return 0
    
class Box_3D(Shape):
    def __init__(self,dim_width = 0.0,dim_height = 0.0,dim_len = 0.0):
        super().__init__(dim_width,dim_height,dim_len)
