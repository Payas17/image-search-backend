import requests
import shutil

import config
from app.product_image import ProductImage
from config import settings


class Product:

    def __init__(self, _id, url, images):
        self.id = _id
        self.url = url
        self.images = []
        self.create_images(images)

    def get_first_image_dir(self):
        return settings.image_path + self.id + ".jpg"

    def create_images(self, images):
        for idx, image_url in enumerate(images[0:config.settings.images_amount]):
            response = requests.get(image_url, stream=True)
            if response.status_code != 200:
                continue
            product_image = ProductImage(image_url, self.id, idx, response.raw)
            self.images.append(product_image)
