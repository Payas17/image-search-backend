from config import settings
import os
import torch


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
		if os.path.exists(settings.full_detection_result):
			os.remove(settings.full_detection_result)
		model = torch.hub.load('ultralytics/yolov5', 'custom', path=path_to_weight)
		results = model(self.path)
		if results.pandas().xyxy[0].empty:
			return None

		return results.pandas().xyxy[0]['name'][0]
