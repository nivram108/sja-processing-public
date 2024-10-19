from PIL import Image

from src.common.configs.config import image_file_extension, annotation_file_extension
from src.common.models.annotation import Annotation
from src.common.models.object_detection_result import ObjectDetectionResult
from src.common.models.unit_image import UnitImage
from src.common.services.file_manager import FileManager


class CropImageService:
    """
    The goal of CropImage is cropping the unit image from the input image.
    """

    # __init__ and enums will be added
    def __init__(self, file_manager: FileManager):
        self.unit_image_list: list[UnitImage] = []
        self.file_manager = file_manager

    def crop_image(self, annotation: Annotation):

        """
        update data of unit image
        :return:
        """
        object_detection_results = annotation.object_detection_results
        object_id = 0
        for detected_object in object_detection_results:
            # open file
            img = Image.open(self.file_manager.
                             get_image_path_from_annotation_filename(detected_object.full_filename))
            # crop image
            cropped_image = img.crop(detected_object.boundary.get_coords())
            cropped_image_filename = self.build_unit_image_file_name(detected_object, object_id)
            unit_image = UnitImage(detected_object, cropped_image_filename, object_id)
            object_id += 1
            # Save the cropped image
            cropped_image.save(unit_image.unit_image_full_filename)
            # TODO: save unit image data
            self.unit_image_list.append(unit_image)

    def build_unit_image_file_name(self, detected_object: ObjectDetectionResult, object_id: int):
        """
        build crop image file name by annotation filename, object index, and class name
        :param detected_object: one detected object in the annotation
        :param object_id: object index
        :return: cropped image file name
        """
        self.file_manager.create_cropped_class_name_folder(detected_object.class_name)
        cropped_image_filename = f"{detected_object.full_filename.replace(f'.{annotation_file_extension}', '')}" \
                                 f"_{object_id}_{detected_object.class_name}." \
                                 f"{image_file_extension}".split('/')[-1]

        return cropped_image_filename
