from logging import DEBUG

from src.common.configs.config import ocr_max_pixels, concat_blank_height, image_file_extension, ocr_height
from src.common.models.dimension import Dimension
from src.common.models.object_boundary import ObjectBoundary
from src.common.models.unit_image import UnitImage
from src.common.services.file_manager import FileManager
from src.common.services.file_processor import FileProcessor
from src.common.services.log_manager import set_up_logger
from src.ocr.models.image_combine_collection import ImageCombineCollection
from src.ocr.models.image_combine_unit_record import ImageCombineUnitRecord
from PIL import Image


class ImageCombineService:
    """
    ImageCombineService is to read the file of list of unit images, and combine then into a large ImageCombineCollection
    that and write to file that is ready to being processed by OCR service
    """

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.unit_images_map_by_class: dict[str, list[UnitImage]] = {}
        self.image_combine_collection_map_by_class: dict[str, list[ImageCombineCollection]] = {}
        self.max_width_map_by_class: dict[str, int] = {}
        self.logger = set_up_logger(__name__)

    def build_unit_image_map_by_class(self, unit_image_list: list[UnitImage]):
        self.logger.debug(f"build unit image map")
        for unit_image in unit_image_list:
            if unit_image.class_name not in self.unit_images_map_by_class:
                self.unit_images_map_by_class[unit_image.class_name] = []
                self.max_width_map_by_class[unit_image.class_name] = 0
            self.unit_images_map_by_class[unit_image.class_name].append(unit_image)
            self.max_width_map_by_class[unit_image.class_name] = max(self.max_width_map_by_class[unit_image.class_name],
                                                                     unit_image.dimension.x)

    def build_image_combine_collection_map(self):
        for class_name in self.unit_images_map_by_class:
            unit_images = self.unit_images_map_by_class[class_name]

            # create multiple combine lists for one class
            # each combine list will be one combine collection
            self.image_combine_collection_map_by_class[class_name] = (
                self.unit_images_to_image_combine_collection_list(class_name,
                                                                  unit_images,
                                                                  self.max_width_map_by_class[class_name]))

    def load_unit_images(self, filename: str) -> list[UnitImage]:
        """
        Load the unit images to be combined by from the csv file with filename.
        :param filename: file that holds the unit image information.
        :return: loaded list of unit images.
        """
        # TODO: implement the process method
        unit_images: list[UnitImage] = self.file_process.read_file_to_object(filename)
        return unit_images

    def unit_images_to_image_combine_collection_list(self, class_name: str, unit_images: list[UnitImage],
                                                     max_width: int) \
            -> list[ImageCombineCollection]:
        """
        Process the unit images and calculated the position (boundary) of each ImageCombineUnitRecord after combined.
        :param class_name: class name of the unit images.
        :param unit_images: unit images to be combined.
        :param max_width: max width of the unit images.
        :return: multiple list of ImageCombineUnitRecord, that is, ImageCombineCollection.
        """
        self.logger.info(f"build image unit record lists for class {class_name}")
        concat_height = 0
        max_height = ocr_height
        image_combine_collection_list: list[ImageCombineCollection] = []  # list of (list of record)
        current_record_list: list[ImageCombineUnitRecord] = []
        image = Image.new('RGB', (max_width, max_height))  # create empty image with max size
        for unit_image in unit_images:
            image.paste(Image.open(unit_image.unit_image_full_filename), (0, concat_height))
            boundary = ObjectBoundary(x_min=0,
                                      y_min=concat_height,
                                      x_max=max_width,
                                      y_max=concat_height + unit_image.dimension.y)
            current_record_list.append(ImageCombineUnitRecord(unit_image, boundary))
            concat_height += unit_image.dimension.y + concat_blank_height

            if concat_height > max_height:  # save concat image with current combine record list
                self.logger.info("Oversize image")
                filename = self.build_concat_image_filename(class_name, len(image_combine_collection_list))
                # oversize, build a new list of combine records
                image_combine_collection_list.append(ImageCombineCollection(current_record_list,
                                                                            Dimension(max_width, concat_height),
                                                                            filename))
                self.save_concat_image(filename, concat_height, image, max_width)
                # reset current list and height
                image = Image.new('RGB', (max_width, max_height))
                concat_height = 0
                current_record_list = []

        if current_record_list:  # save concat image with leftover current combine record list
            filename = self.build_concat_image_filename(class_name, len(image_combine_collection_list))
            # oversize, build a new list of combine records
            image_combine_collection_list.append(ImageCombineCollection(current_record_list,
                                                                        Dimension(max_width, concat_height), filename))
            self.save_concat_image(filename, concat_height, image, max_width)
        image.close()
        return image_combine_collection_list

    def save_concat_image(self, filename: str, concat_height: int, image: Image, max_width: int):
        self.logger.info(f"save concat image {filename}")
        save_image = image.crop((0, 0, max_width, concat_height))
        save_image.save(filename)
        save_image.close()

    def write_combine_collection_result(self, combine_collection: ImageCombineCollection):
        """
        Write the combine collection into csv that is OCR-process ready
        :param combine_collection: the combine collection that is ready to be processed by OCR process
        """
        # TODO: combine the actual image and save the combined image, and update the filename in combine_collection
        pass

    def build_concat_image_filename(self, classname: str, index: int):

        self.file_manager.create_concat_class_name_folder(classname)
        filename = f"{self.file_manager.get_concat_class_name_folder(classname)}/concat_{index}.{image_file_extension}"
        self.logger.info(f"concat image filename: {filename}")
        return filename
