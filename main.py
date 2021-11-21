from app.image_searcher import ImageSearcher
from config import settings
import os

def get_file(file_name):
		path = os.path.abspath(os.path.dirname(__file__))
		file_path = path +'/test_images/' + file_name
		return open(file_path, 'rb')

def clean_tasks():
	os.remove(settings.full_detection_result)


file_name = 'mate4.jpg'
file = get_file(file_name)
image_searcher = ImageSearcher(file)
label = image_searcher.identify_object()
if not label:
	print("objeto no encontrado")
else:
	image_searcher.search_products(label)
	image_searcher.download_products_pictures()
	url = image_searcher.get_similar_product_url()
	print(url)
