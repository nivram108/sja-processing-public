import os
import unittest

from root import root_dir
from src.common.models.annotation import Annotation
from src.common.services.crop_image_service import CropImageService
from src.common.services.file_manager import FileManager


class TestCropImageService(unittest.TestCase):

    def setUp(self):
        self.file_manager = FileManager()
        self.crop_image_service = CropImageService(self.file_manager)

    def test_crop_image(self):
        filename = f'{root_dir}' \
                   f'/tests/test_resources/annotations/U15_72_1615507509000-2021-03-12-08-05-09-373-Facebook.xml'
        annotation = Annotation(filename)
        self.crop_image_service.crop_image(annotation)

