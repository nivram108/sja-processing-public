import os
import unittest

from root import root_dir
from src.common.models.annotation import Annotation
from src.common.services.file_manager import FileManager


class TestFileManager(unittest.TestCase):

    def test_create_folders(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        file_manager = FileManager()

    def test_build_filename(self):
        filename = f'{root_dir}' \
                   f'/tests/test_resources/annotations/U15_72_1615507509000-2021-03-12-08-05-09-373-Facebook.xml'
        annotation = Annotation(filename)
        print(FileManager.get_image_path_from_annotation_filename(filename))
