import unittest
import os.path
import os

from src.common.models.annotation import Annotation


class TestAnnotation(unittest.TestCase):

    def test_build_annotation(self):
        filename = '../../test_resources/annotations/U15_72_1615507509000-2021-03-12-08-05-09-373-Facebook.xml'
        annotation = Annotation(filename)
        self.assertEqual(9, len(annotation.object_detection_results))
        self.assertEqual(0.8, annotation.object_detection_results[0].confidence)
        self.assertEqual(0.8, annotation.object_detection_results[0].confidence)
        self.assertEqual(65758, annotation.object_detection_results[0].get_area())
        print()