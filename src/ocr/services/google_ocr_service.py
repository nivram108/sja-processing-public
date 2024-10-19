import json
import os
from pprint import pprint

from google.cloud.vision_v1 import EntityAnnotation

from src.common.configs.config import ocr_credential_path, context_space_pixels
from src.common.models.object_boundary import ObjectBoundary
from src.common.services.log_manager import set_up_logger
from src.ocr.models.ocr_result import OcrResult
from src.ocr.models.image_combine_collection import ImageCombineCollection
from google.cloud import vision
from google.cloud.vision import AnnotateImageResponse

from src.ocr.models.text_annotation import TextAnnotation


class GoogleOcrService:
    def __init__(self):
        self.logger = set_up_logger(__name__)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ocr_credential_path
        self.api_client = vision.ImageAnnotatorClient()

    def load_combine_result(self, filename: str):
        pass

    def process_combine_image_ocr(self, image_combine_collection: ImageCombineCollection):
        ocr_result = self.generate_google_ocr(image_combine_collection)
        unit_record_process_boundary_map: dict[str, ObjectBoundary] = {}  # recording the processed text area
        for text_annotation in ocr_result.text_annotations:
            for image_combine_unit_record in image_combine_collection.unit_records:
                if image_combine_unit_record.boundary.is_including(text_annotation.boundary):
                    unit_image = image_combine_unit_record.unit_image
                    if unit_image.unit_image_full_filename not in unit_record_process_boundary_map:
                        unit_record_process_boundary_map[unit_image.unit_image_full_filename] \
                            = ObjectBoundary(image_combine_unit_record.boundary.x_min,
                                             image_combine_unit_record.boundary.y_min,
                                             image_combine_unit_record.boundary.x_min,
                                             image_combine_unit_record.boundary.y_min)
                    # check if annotation is already included in the unit record
                    if not unit_record_process_boundary_map[unit_image.unit_image_full_filename].is_including(
                            text_annotation.boundary):
                        # detect space
                        if unit_record_process_boundary_map[unit_image.unit_image_full_filename].x_max < \
                              text_annotation.boundary.x_min - context_space_pixels and unit_image.text:
                            unit_image.text += " "

                        unit_image.text += text_annotation.description
                        unit_record_process_boundary_map[unit_image.unit_image_full_filename] \
                            = ObjectBoundary(image_combine_unit_record.boundary.x_min,
                                             image_combine_unit_record.boundary.y_min,
                                             text_annotation.boundary.x_max,
                                             text_annotation.boundary.y_max)
                    else:
                        print(f"Already processed: {image_combine_unit_record.boundary.get_coords()} > "
                              f"{text_annotation.boundary.get_coords()}")

        for image_combine_unit_record in image_combine_collection.unit_records:
            if image_combine_unit_record.unit_image.text:
                print(f"unit image: {image_combine_unit_record.unit_image.unit_image_full_filename} -> "
                      f"{image_combine_unit_record.unit_image.text}")

    def generate_google_ocr(self, image_combine_collection: ImageCombineCollection) -> OcrResult:
        self.logger.info(f"Processing Google OCR for file {image_combine_collection.filename}")
        return OcrResult.build_from_google_ocr_annotations(image_combine_collection.filename,
                                                           self.unit_image_ocr(image_combine_collection.filename))

    def unit_image_ocr(self, filename: str) -> list[EntityAnnotation]:

        with open(filename, "rb") as image_file:
            content = image_file.read()

        image = vision.Image()
        image.content = content
        response = self.api_client.text_detection(image=image)
        # serialize / deserialize proto (binary)
        serialized_proto_plus = AnnotateImageResponse.serialize(response)
        response = AnnotateImageResponse.deserialize(serialized_proto_plus)

        # serialize / deserialize json
        response_json = AnnotateImageResponse.to_json(response)
        texts: list[EntityAnnotation] = response.text_annotations
        # ocr_tmp_result = open(filename.replace('.jpg', '.txt'), "w", encoding="utf-8")
        # ocr_tmp_result.write(json.dumps(response_json))
        with open(filename.replace('.jpg', '.json'), "w", encoding="utf8") as json_file:
            json.dump(response_json, json_file, ensure_ascii=False)
        # for text in texts:
        #     vertices = [
        #         f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        #     ]
        #     print(f"{vertices}  -> {text.description}")
        return texts
