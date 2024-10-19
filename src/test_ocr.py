from src.ocr.services.google_ocr_service import GoogleOcrService

ocr_service = GoogleOcrService()
file = 'your-image-path'
print(ocr_service.unit_image_ocr(file)[0].description)
