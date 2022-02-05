from io import BytesIO

import torch
from PIL import Image

import config
from config import settings


class Identifier:

	def __init__(self, searched_image):
		self.path = f"{settings.searched_image_folder}{settings.searched_image_name}.jpg"
		with open(self.path, 'wb') as f:
			f.write(searched_image)

	def get_object(self):
		label = self.detect_object()
		return label

	def detect_object(self):
		path_to_weight = settings.weight_path
		model = torch.hub.load('ultralytics/yolov5', 'custom', path=path_to_weight)
		results = model(self.path)
		if config.settings.debug:
			self.save_results(results)
		if results.pandas().xyxy[0].empty:
			return None
		return results.pandas().xyxy[0]['name'][0]

	def save_results(self, results):
		results.render()  # updates results.imgs with boxes and labels
		for img in results.imgs:

			buffered = BytesIO()
			img_base64 = Image.fromarray(img)
			img_base64.save(buffered, format="JPEG")
			with open(f"{config.settings.full_detection_result}detected_image.JPEG", "wb") as f:
				f.write(buffered.getvalue())


