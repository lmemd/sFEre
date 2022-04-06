class generic_box:
    """
    This class describes the modeled sphere, either it is in 2 or 3 dimensions,
    """
    
    sides = (0, 0, 0)
    def __init__(self, *args):
        self.sides = args or self.sides
    
    @property
    def ndim(self):
        return len(self.sides)

class box_2D(generic_box):
    sides = (0, 0)
        
class box_3D(generic_box):
    pass
