from src.common.models.dimension import Dimension
from src.common.models.object_boundary import ObjectBoundary
from src.common.models.object_detection_result import ObjectDetectionResult
from src.common.services.file_manager import FileManager


class UnitImage:
    """
    UnitImage is the snipped image from the original screenshot.

    ----

    Attributes:

    annotation_full_filename: str
     originated annotation file name with full path
    unit_image_full_filename: str
     saved unit image filename with full path
    object_id: int
     the index order of the unit image in the originated annotation
    class_name: sts
     the class name of this unit image
    dimension: Dimension
     the dimension (size) of the unit image.
    boundary: ObjectBoundary
     the boundary (position) of the unit image in the original image
    """
    annotation_full_filename: str
    unit_image_full_filename: str
    object_id: int
    class_name: str
    dimension: Dimension
    boundary: ObjectBoundary
    text: str

    def __init__(self, object_detection_result: ObjectDetectionResult, unit_image_filename: str, object_id: int):
        self.annotation_full_filename = object_detection_result.full_filename
        self.dimension = Dimension(object_detection_result.boundary.x_max - object_detection_result.boundary.x_min,
                                   object_detection_result.boundary.y_max - object_detection_result.boundary.y_min)
        self.class_name = object_detection_result.class_name
        self.boundary = object_detection_result.boundary
        self.object_id = object_id
        self.unit_image_full_filename = f"{FileManager.get_cropped_class_name_folder(self.class_name)}/" \
                                        f"{unit_image_filename}"
        self.text = ""

    def dict(self):
        return {
            'annotation_full_filename': self.annotation_full_filename,
            'unit_image_full_filename': self.unit_image_full_filename,
            'class_name': self.class_name,
            'dimension': self.dimension.__dict__,
            'boundary': self.boundary.__dict__,
            'text': self.text
        }