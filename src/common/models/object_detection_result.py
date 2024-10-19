from src.common.models.object_boundary import ObjectBoundary


class ObjectDetectionResult:
    """
    ObjectDetectionResult will be the outcome from the yolo detection.
    This will also be used as the input for OCR process
    ObjectDetectionResult will hold information for a detected object

    ----

    Attributes:

    full_filename: str
     filename of the belonged annotation file including full path
    boundary: ObjectBoundary
     its position and boundary in the original image
    class_name: str
     detected object class
    confidence: float
     confidence value from the object detection
    """

    full_filename: str
    boundary: ObjectBoundary
    class_name: str
    confidence: float

    def __init__(self, full_filename, obj):
        self.full_filename = full_filename
        self.class_name = obj.find("name").text
        self.confidence = float(obj.find("confidence").text) if obj.find("confidence") else 1.0
        self.boundary = ObjectBoundary(
            int(obj.find("xmin").text),
            int(obj.find("ymin").text),
            int(obj.find("xmax").text),
            int(obj.find("ymax").text),
        )

    def get_area(self) -> int:
        return self.boundary.get_area()
