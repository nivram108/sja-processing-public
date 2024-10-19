from bs4 import BeautifulSoup

from src.common.models.object_detection_result import ObjectDetectionResult


class Annotation:
    """
    IdentifiedScreenshot is the identified/classified image from the original
    image, formed with ObjectDetectionResult.

    ---
    Attributes:

    full_filename: str
      filename with full path of the annotation file
    object_detection_results: list[ObjectDetectionResult]
      list of object detection result in the annotation
    width: int
      horizontal dimension of the annotated image
    height: int
      vertical dimension of the annotated image
    """

    full_filename: str
    object_detection_results: list[ObjectDetectionResult]
    width: int
    height: int

    def __init__(self, filename):
        self.load_annotation(filename)

    def build_annotation(self, full_filename, objects, bs_data):
        self.full_filename = full_filename
        self.object_detection_results = objects
        self.height = int(bs_data.find('height').text)
        self.width = int(bs_data.find('width').text)

    def load_annotation(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
        object_detection_results: list[ObjectDetectionResult] = []
        bs_data = BeautifulSoup(data, 'xml')
        for obj in bs_data.find_all("object"):
            try:
                object_detection_results.append(ObjectDetectionResult(filename, obj))
            except Exception as e:
                print(e)

        self.build_annotation(full_filename=filename,
                              objects=object_detection_results,
                              bs_data=bs_data
                              )
