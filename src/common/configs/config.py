import logging
import os
from root import root_dir
cwd = os.getcwd()

resource_path = 'resources'
annotations_path = f'{resource_path}/annotations'
output_path = f'{root_dir}/output'
cropped_image_path = f'{output_path}/crop'
concat_image_path = f'{output_path}/concat'
result_path = f'{output_path}/results'
image_file_extension = "jpg"
result_file_extension = "json"
annotation_file_extension = "xml"
ocr_max_pixels = 60000000
ocr_height = 20000
concat_blank_height = 50
log_level = logging.DEBUG
ocr_credential_path = f"{cwd}\\..\\news-consumption-d146b044fe1b.json"
context_space_pixels = 10
