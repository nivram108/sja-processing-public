""" Description of ScreenshotResult and subclasses
ScreenshotResult is the processed result of the screenshot, that is, its unit images information
which includes object detection and ocr content
subclasses are for customizing specific usage of ScreenshotResult
"""
import json
from functools import cmp_to_key

from src.common.models.unit_image import UnitImage


class ScreenshotResult:
    unit_images: list[UnitImage]
    filename: str
    sequence_id: int

    def __init__(self, unit_images: list[UnitImage], filename: str, sort_unit_image: bool = False):
        self.unit_images = unit_images
        if sort_unit_image:
            self.unit_images.sort(key=cmp_to_key(lambda x, y: x.boundary.y_min - y.boundary.y_min))
        self.filename = filename

    def to_dict(self):
        data = {
            # 'filename': self.filename,
            'filename': self.filename.split('/')[-1].split('.')[0],
            'content': [
                {
                    'class_name': u.class_name,
                    'boundary': u.boundary.get_coords(),
                    'text': u.text
                } for u in self.unit_images
            ]
        }
        return data

    def to_json(self):
        return json.dumps(self.to_dict())


class NewsInterestScreenshotResult(ScreenshotResult):
    is_news: bool
