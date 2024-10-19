from src.ocr.services.google_ocr_service import GoogleOcrService

ocr_service = GoogleOcrService()
file = 'C:\projects\sja\sja_processing\output\concat\\fb_interaction_count\concat_0.jpg'
ocr_service.unit_image_ocr(file)
