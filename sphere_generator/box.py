class generic_box:
    """
    This class describes the modeled sphere, either it is in 2 or 3 dimensions,
    """
      
    def __init__(self, sides = (0, 0, 0), offsets = (0, 0, 0)):
        self.sides =  sides
        self.offsets = offsets

    @property
    def ndim(self):
        return len(self.sides)

class box_2D(generic_box):
    def __init__(self,sides = (0, 0), offsets = (0,0)):
        super().__init__(sides,offsets)
        
class box_3D(generic_box):
    def __init__(self, sides = (0, 0, 0), offsets = (0, 0, 0)):
        super().__init__(sides,offsets)

#debugging code

box = box_2D((1,1))
print(box.sides)
print(box.ndim)
print(box.offsets)

box_2 = box_3D(sides = (1,1,1))
print(box_2.ndim)