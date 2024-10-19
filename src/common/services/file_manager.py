import logging
import os

from src.common.configs import config
from src.common.services.log_manager import set_up_logger
import shutil

class FileManager:
    """
    FIle Manager handles helper functions to create and organize files and folders
    """
    def __init__(self):
        self.logger = set_up_logger(__name__)
        self.unit_image_class_name_folder_exist_set = set()
        self.concat_image_class_name_folder_exist_set = set()
        self._create_init_folders()

    @staticmethod
    def get_cropped_class_name_folder(class_name: str):
        return f"{config.cropped_image_path}/{class_name}"

    @staticmethod
    def get_concat_class_name_folder(class_name: str):
        return f"{config.concat_image_path}/{class_name}"

    @staticmethod
    def get_image_path_from_annotation_filename(annotation_filename: str) -> str:
        return annotation_filename.replace("/annotations/", '/images/') \
            .replace(f'.{config.annotation_file_extension}', f'.{config.image_file_extension}')
    @staticmethod
    def get_result_path_from_annotation_filename(annotation_filename: str) -> str:
        return annotation_filename.replace("/resources/annotations/", "/output/results/") \
            .replace(f'.{config.annotation_file_extension}', f'.{config.result_file_extension}')
    @staticmethod
    def get_annotation_filename_from_image_filename(image_filename: str) -> str:
        return image_filename.replace("/images/", '/annotations/')\
            .replace(f'.{config.image_file_extension}', f'.{config.annotation_file_extension}')

    def create_cropped_class_name_folder(self, class_name: str) -> str:
        cropped_class_name_folder = f"{config.cropped_image_path}/{class_name}"
        if class_name not in self.unit_image_class_name_folder_exist_set:
            self.unit_image_class_name_folder_exist_set.add(class_name)
            self._create_folder_if_not_exist(cropped_class_name_folder)
        return cropped_class_name_folder

    def create_concat_class_name_folder(self, class_name: str) -> str:
        concat_class_name_folder = f"{config.concat_image_path}/{class_name}"
        if class_name not in self.concat_image_class_name_folder_exist_set:
            self.concat_image_class_name_folder_exist_set.add(class_name)
            self._create_folder_if_not_exist(concat_class_name_folder)
        return concat_class_name_folder

    def _create_init_folders(self):
        self._create_folder_if_not_exist(config.output_path)
        self._create_folder_if_not_exist(config.cropped_image_path)
        self._create_folder_if_not_exist(config.concat_image_path)
        self._create_folder_if_not_exist(config.result_path)

    def _create_folder_if_not_exist(self, path):
        try:
            self.logger.info(f"creating folder {path}")
            os.mkdir(path)
        except FileExistsError as ex:
            self.logger.warning(f"{path} folder already exist")

    def copy_file(self, filename:str, dest: str):
        try:
            shutil.copy2(filename, dest)
        except Exception as ex:
            self.logger.warning(f"copy file failed: {filename}")
