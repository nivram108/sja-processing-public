from src.common.models.dimension import Dimension
from src.ocr.models.image_combine_unit_record import ImageCombineUnitRecord


class ImageCombineCollection:
    """
    Image combine record of a single unit image.
    ImageCombineCollection is consists of many ImageCombineUnitRecord with the same class

    ----

    Attributes:

    filename: str
     the saved combined image file name
    unit_records: list[ImageCombineUnitRecord]
     list of collected unit records in this image combine collection
    dimension: Dimension
     the dimension (size) of the combined collection image.
    """

    filename: str
    unit_records: list[ImageCombineUnitRecord]
    dimension: Dimension

    def __init__(self,
                 unit_records: list[ImageCombineUnitRecord],
                 dimension: Dimension,
                 filename: str):
        self.unit_records = unit_records
        self.dimension = dimension
        self.filename = filename
