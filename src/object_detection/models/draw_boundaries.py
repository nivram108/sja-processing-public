from src.common.models.object_detection_result import ObjectDetectionResult
from src.common.models.image_status import ImageStatus
from PIL import Image, ImageDraw


class RecordBoundaries:
    """(image: class IdentifiedScreenshot)"""
    # if meeting a detected object, record its position

    def __init__(self):
        self.status = ImageStatus.INITIATED

    # We want to see the boundaries on the screenshot

    def record_boundary(self, detected_image: ObjectDetectionResult) -> Image.Image:
        # open file
        img = Image.open(detected_image.full_filename)

        # create a file editor
        draw = ImageDraw.Draw(img)

        # draw boundary
        draw.rectangle([detected_image.boundary.x_min, detected_image.boundary.y_min,
                        detected_image.boundary.x_max, detected_image.boundary.y_max], outline='red', width=2)

        # save image
        img.save('boxed_image.jpg')

        # image status: DREW
        self.status = ImageStatus.DREW
        # show image
        # img.show()
        return img


