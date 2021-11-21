import requests
import json


class MercadolibreSearcher:
		BASE_URL = "https://api.mercadolibre.com/sites/MLA/search?q="
		ITEMS_URL = "https://api.mercadolibre.com/items?attributes=id,permalink,pictures.url&ids="
		
		def search(self, search_query, offset=0, limit=10):
				ids = self.get_products_ids(search_query, offset, limit)
				response = self.search_products(ids)
				return self.get_products(response)

		def get_products_ids(self, search_query, offset=0, limit=10):
 				url = self.BASE_URL + search_query + self.add_offset(offset) + self.add_limit(limit)
 				headers = {'Content-type': 'application/json'}
 				response = requests.get(url, headers=headers)
 				response_data = json.loads(response.content)
 				ids = []
 				for product in response_data['results']:
 						ids.append(product['id'])
 				return ids

		def search_products(self, ids):
 				ids_string = ""
 				for product_id in ids:
 						ids_string += product_id + ','
 				url = self.ITEMS_URL + ids_string
 				headers = {'Content-type': 'application/json'}
 				response = requests.get(url, headers=headers)
 				return json.loads(response.content)

		def add_offset(self, offset):
	  		return f"&offset={offset}"

		def add_limit(self, limit):
	  		return f"&limit={limit}"

		def get_products(self, response):
	  		products = []
	  		for product in response:
	  				product = product['body']
	  				product_dict = {'id': product['id'], 
	  												'url': product['permalink'], 
	  												'images': self.get_product_images_urls(product['pictures']) }
	  				products.append(product_dict)
	  		return products

		def get_product_images_urls(self, pictures):
	  		urls = []
	  		for picture in pictures:
	  				urls.append(picture['url'])
	  		return urls








