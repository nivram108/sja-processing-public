import json
import os
from pprint import pprint

from root import root_dir
from src.common.configs.config import annotations_path, result_path
from src.common.models.annotation import Annotation
from src.common.models.unit_image import UnitImage
from src.common.services.crop_image_service import CropImageService
from src.common.services.file_manager import FileManager
from src.ocr.services.google_ocr_service import GoogleOcrService
from src.ocr.services.image_combine_service import ImageCombineService
from src.result_builder.models.screenshot_result import NewsInterestScreenshotResult

debug = True
result_image_reference = True
# define service classes
file_manager = FileManager()
crop_image_service = CropImageService(file_manager)
image_combine_service = ImageCombineService(file_manager)
ocr_service = GoogleOcrService()

# load annotation files
path = f"{root_dir}/{annotations_path}"
annotation_files = os.listdir(path)
if debug:
    annotation_files = annotation_files[:10]

# annotation_files = [annotation_files[2]]

# crop annotation files into unit images and concat them into large image for same object detection class
for annotation_file in annotation_files:
    annotation = Annotation(f"{path}/{annotation_file}")
    crop_image_service.crop_image(annotation)
print(crop_image_service.unit_image_list[0].unit_image_full_filename)
image_combine_service.build_unit_image_map_by_class(crop_image_service.unit_image_list)
image_combine_service.build_image_combine_collection_map()

# parse ocr and get text result for every unit image
for class_name in image_combine_service.image_combine_collection_map_by_class:
    for record in image_combine_service.image_combine_collection_map_by_class[class_name]:
        ocr_service.process_combine_image_ocr(record)

# recombine the unit image with text result into originated annotation file
unit_images_by_name_map: dict[str, list[UnitImage]] = {}
for image_combine_collection_list in image_combine_service.image_combine_collection_map_by_class.values():
    for image_combine_collection in image_combine_collection_list:
        for unit_record in image_combine_collection.unit_records:
            if unit_record.unit_image.annotation_full_filename not in unit_images_by_name_map:
                unit_images: list[UnitImage] = []
            else:
                unit_images = unit_images_by_name_map[unit_record.unit_image.annotation_full_filename]
            unit_images.append(unit_record.unit_image)
            unit_images_by_name_map[unit_record.unit_image.annotation_full_filename] = unit_images


# build screenshot results
news_interest_screenshot_results: list[NewsInterestScreenshotResult] = []
for annotation_name in unit_images_by_name_map:
    news_interest_screenshot_results.append(NewsInterestScreenshotResult(unit_images_by_name_map[annotation_name],
                                                                         annotation_name, sort_unit_image=True))

for result in news_interest_screenshot_results:
    if result_image_reference:
        image_filename = file_manager.get_image_path_from_annotation_filename(result.filename)
        file_manager.copy_file(image_filename, result_path)
    else:
        print(f"Image: {result.filename.replace('annotations', 'images').replace('xml', 'jpg')}")
    # with open(file_manager.get_result_path_from_annotation_filename(result.filename), "w") as result_file:
    #     json.dump(result.to_dict(), indent=4, fp=result_file, ensure_ascii=False)

    f = open(file_manager.get_result_path_from_annotation_filename(result.filename), "w", encoding="utf-8")
    f.write(json.dumps(result.to_dict(), indent=4, ensure_ascii=False))
    f.close()
    # pprint(result.to_dict())
# save unit image results
# ocr_ready_unit_images = csv.read('unit_image_results.csv')
# ocr_service.process_ocr(crop_image_service.unit_image_list)
