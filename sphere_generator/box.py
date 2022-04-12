class generic_box:
    """
    This class describes the modeled sphere, either it is in 2 or 3 dimensions,
    """
      
    def __init__(self, sides = (0, 0, 0)):
        self.sides =  sides

    @property
    def ndim(self):
        return len(self.sides)

class box_2D(generic_box):
    def __init__(self,sides = (0, 0)):
        super().__init__(sides)
        
class box_3D(generic_box):
    def __init__(self, sides = (0, 0, 0)):
        super().__init__(sides)

#debugging code

box = box_2D((1,1))
print(box.sides)
print(box.ndim)

box_2 = box_3D(sides = (1,1,1))
print(box_2.ndim)