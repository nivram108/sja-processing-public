from src.common.models.object_boundary import ObjectBoundary
from src.common.models.unit_image import UnitImage


class ImageCombineUnitRecord:
    """
    Image combine record of a single unit image.
    ImageCombineCollection is consists of many ImageCombineUnitRecord with the same class

    ----

    Attributes:

    unit_image: UnitImage
     the unit image of this combine unit record
    boundary: ObjectBoundary
     the boundary and position of this unit record in the ImageCombineCollection
    """
    unit_image: UnitImage
    boundary: ObjectBoundary

    def __init__(self, unit_image: UnitImage, boundary: ObjectBoundary):
        self.unit_image = unit_image
        self.boundary = boundary
