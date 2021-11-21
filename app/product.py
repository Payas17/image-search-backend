import requests
import shutil
from config import settings

class Product:

	def __init__(self, _id, url, images):
		self.id = _id
		self.url = url
		self.images = images

	def save_picture(self, url):
		response = requests.get(url, stream=True)
		save_path = settings.image_path + self.id + ".jpg"
		if response.status_code == 200:
			with open(save_path, 'wb') as f:
				response.raw.decode_content = True
				shutil.copyfileobj(response.raw, f)

	def get_pictures(self):
		for image in self.images[0:1]:
			self.save_picture(image)

	def get_first_image_dir(self):
		return settings.image_path + self.id + ".jpg"

	def get_featured_vector_dir(self):
		return settings.image_path + self.id + ".npz"

