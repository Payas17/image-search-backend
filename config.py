import os
from functools import lru_cache

from pydantic import BaseSettings
from fastapi.templating import Jinja2Templates


def get_abs_path():
    return os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    image_path = get_abs_path() + '/images/'
    weight_path = get_abs_path() + '/weights/best.pt'
    yolo_detect_path = get_abs_path() + '/notebooks/identifier/yolov5/'
    searched_image_name = 'searched_image'
    searched_image_folder = 'searched_image/'
    searched_image_folder_path = get_abs_path() + f'/{searched_image_folder}'
    searched_image_path = get_abs_path() + f'/{searched_image_folder}' + searched_image_name + '.jpg'
    searched_featured_vector_path = get_abs_path() + f'/{searched_image_folder}' + searched_image_name +'.npz'
    detection_path = 'detection'
    full_detection_result = get_abs_path() + f"/{detection_path}/"
    feature_vectors_path = get_abs_path() + "/feature-vectors/"
    jsons_path = get_abs_path() + "/jsons/named_nearest_neighbors.json"
    templates = Jinja2Templates(directory="front/templates")
    products_amount = 10
    images_amount = 3
    debug = True

@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
