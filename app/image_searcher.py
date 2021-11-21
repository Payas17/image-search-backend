from .product import Product
from .search import MercadolibreSearcher
from .identifier import Identifier
from .comparator import Comparator
import os


class ImageSearcher:

	def __init__(self, image_to_search):
		self.products = []
		self.identifier = Identifier(image_to_search)
		self.searcher = MercadolibreSearcher()
		self.comparator = Comparator(image_to_search)

	def identify_object(self):
		return self.identifier.get_object()

	def search_products(self, search_string, offset=0, limit=10):
		products_data = self.searcher.search(search_string, offset, limit)
		self.create_products(products_data)
		return self.products

	def create_products(self, products_dict):
		for product_dict in products_dict:
			product = Product(product_dict['id'], product_dict['url'], product_dict['images'])
			self.products.append(product)

	def download_products_pictures(self):
		for product in self.products:
			product.get_pictures()

	def get_similar_product_url(self):
		product = self.comparator.get_similar_product(self.products)
		return product.url
