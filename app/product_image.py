import shutil

import config
from config import settings


class ProductImage:

    def __init__(self, url, product_id, image_id, file):
        self.url = url
        self.product_id = product_id
        self.id = image_id
        self.file = file
        self.file_name = self.product_id + "_" + str(self.id)
        self.file_path = settings.image_path + self.file_name + ".jpg"
        self.save_image()

    def save_image(self):
        save_path = settings.image_path + self.product_id + "_" + str(self.id) + ".jpg"
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(self.file, f)
        self.file_path = save_path

    def get_image_name(self):
        return self.file_name

    def get_featured_vector_dir(self):
        return settings.image_path + self.file_name + ".npz"
