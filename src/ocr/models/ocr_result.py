from google.cloud.vision_v1 import EntityAnnotation

from src.ocr.models.text_annotation import TextAnnotation


class OcrResult:
    """
    Holds the return results from Google OCR
    """
    filename: str
    text_annotations: list[TextAnnotation]

    def __init__(self, filename: str, text_annotations: list[TextAnnotation]):
        self.filename = filename
        self.text_annotations = text_annotations

    @classmethod
    def build_from_google_ocr_annotations(cls, filename: str, google_ocr_texts: list[EntityAnnotation]):
        text_annotations: list[TextAnnotation] = []
        for text in google_ocr_texts:
            text_annotations.append(TextAnnotation.build_annotation_from_google_annotation(text))
        return cls(filename, text_annotations)
