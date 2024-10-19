from src.ocr.models.ocr_result import OcrResult
from src.ocr.models.image_combine_collection import ImageCombineCollection
from src.ocr.models.image_text_result import ImageTextResult


class OcrResultExtractorService:

    def process_ocr_result(self, google_ocr_result: OcrResult, image_combine_collection: ImageCombineCollection)\
            -> ImageTextResult:
        pass
