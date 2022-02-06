# For running inference on the TF-Hub module with Tensorflow
import tensorflow as tf
import tensorflow_hub as hub
# For saving 'feature vectors' into a txt file
import numpy as np
# Glob for reading file names in a folder
import glob
import os.path
# Numpy for loading image feature vectors from file
# Time for measuring the process time
import time
# Glob for reading file names in a folder
# json for storing data in json file
import json
# Annoy and Scipy for similarity calculation
from annoy import AnnoyIndex
from scipy import spatial

import config
from config import settings


class Comparator:

	def __init__(self, searched_image):
		self.searched_image = searched_image

	def get_similar_product(self, products):
		self.get_image_feature_vectors(settings.searched_image_folder_path)
		self.get_image_feature_vectors(settings.image_path)
		product = self.cluster(products)
		return product

#################################################
# This function:
# Loads the JPEG image at the given path
# Decodes the JPEG image to a uint8 W X H X 3 tensor
# Resizes the image to 224 x 224 x 3 tensor
# Returns the pre processed image as 224 x 224 x 3 tensor
#################################################
	def load_img(self, path):
		# Reads the image file and returns data type of string
		img = tf.io.read_file(path)
		# Decodes the image to W x H x 3 shape tensor with type of uint8
		img = tf.io.decode_jpeg(img, channels=3)
		# Resizes the image to 224 x 224 x 3 shape tensor
		img = tf.image.resize_with_pad(img, 224, 224)
		# Converts the data type of uint8 to float32 by adding a new axis
		# img becomes 1 x 224 x 224 x 3 tensor with data type of float32
		# This is required for the mobilenet model we are using
		img = tf.image.convert_image_dtype(img,tf.float32)[tf.newaxis, ...]
		return img


#################################################
# This function:
# Loads the mobilenet model in TF.HUB
# Makes an inference for all images stored in a local folder
# Saves each of the feature vectors in a file
#################################################
	def get_image_feature_vectors(self, images_path):

		# Definition of module with using tfhub.dev
		module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
		# Loads the module
		module = hub.load(module_handle)
		# Loops through all images in a local folder
		for filename in glob.glob(f'{images_path}*.jpg'):
			# Loads and pre-process the image
			img = self.load_img(filename)
			# Calculate the image feature vector of the img
			features = module(img)
			# Remove single-dimensional entries from the 'features' array
			feature_set = np.squeeze(features)

			# Saves the image feature vectors into a file for later use
			outfile_name = os.path.basename(filename).split('.')[0] + ".npz"
			out_path = images_path + outfile_name
			# Saves the 'feature_set' to a text file
			np.savetxt(out_path, feature_set, delimiter=',')


	#################################################
	#################################################
	# This function reads from 'image_data.json' file
	# Looks for a specific 'filename' value
	# Returns the product id when product image names are matched
	# So it is used to find product id based on the product image name
	#################################################
	def match_id(self, filename):
		with open(settings.jsons_path) as json_file:
			for file in json_file:
				seen = json.loads(file)
			for line in seen:
				if filename==line['imageName']:
					return line['productId']
	#################################################
	#################################################
	# This function:
	# Reads all image feature vectores stored in /feature-vectors/*.npz
	# Adds them all in Annoy Index
	# Builds ANNOY index
	# Calculates the nearest neighbors and image similarity metrics
	# Stores image similarity scores with productID in a json file
	#################################################
	def cluster(self, products):
		start_time = time.time()


		print("---------------------------------")
		print ("Step.1 - ANNOY index generation - Started at %s"
		%time.ctime())
		print("---------------------------------")
		# Defining data structures as empty dict
		file_index_to_file_name = {}
		file_index_to_file_vector = {}
		file_index_to_product_id = {}
		# Configuring annoy parameters
		dims = 1792
		n_nearest_neighbors = config.settings.products_amount * config.settings.images_amount
		trees = 10000
		# Reads all file names which stores feature vectors
		allfiles = glob.glob(f'{settings.image_path}*.npz')

		t = AnnoyIndex(dims, metric='angular')

		for index, product in enumerate(products):
			# Reads feature vectors and assigns them into the file_vector
			for image in product.images:
				file_vector = np.loadtxt(image.get_featured_vector_dir())
				# Assigns file_name, feature_vectors and corresponding product_id
				file_name = image.get_image_name()
				file_index = index
				file_index_to_file_name[file_index] = file_name
				file_index_to_file_vector[file_index] = file_vector
				# Adds image feature vectors into annoy index
				t.add_item(file_index, file_vector)
				print("---------------------------------")
				print("Annoy index     : %s" %file_index)
				print("Image file name : %s" %file_name)
				print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))
		print(file_index_to_file_name)
		# Builds annoy index
		t.build(trees)
		print ("Step.1 - ANNOY index generation - Finished")
		print ("Step.2 - Similarity score calculation - Started ")
		named_nearest_neighbors = []

		# Assigns master file_name, image feature vectors
		# and product id values
		master_file_path = settings.searched_image_path
		master_vector = np.loadtxt(settings.searched_featured_vector_path)
		master_index = len(file_index_to_file_name.keys())
		master_file_name = os.path.basename(master_file_path).split('.')[0]
		file_index_to_file_name[master_index] = master_file_name
		file_index_to_file_vector[master_index] = master_vector
		t.add_item(master_index, master_vector)
		# Calculates the nearest neighbors of the master item
		nearest_neighbors = t.get_nns_by_item(master_index, n_nearest_neighbors)
		# Loops through the nearest neighbors of the master item
		for j in nearest_neighbors:
			# Assigns file_name, image feature vectors and
			# product id values of the similar item
			neighbor_file_name = file_index_to_file_name[j]
			neighbor_file_vector = file_index_to_file_vector[j]
			# Calculates the similarity score of the similar item
			similarity = 1 - spatial.distance.cosine(master_vector, neighbor_file_vector)
			rounded_similarity = int((similarity * 10000)) / 10000.0
			# Appends master product id with the similarity score
			# and the product id of the similar items
			named_nearest_neighbors.append({
			'similarity': rounded_similarity,
			'image_id': neighbor_file_name.split("_")[0],
			'image_name': neighbor_file_name,
			'image_index': j})
		print("---------------------------------")
		print("Nearest Neighbors.     : %s" %nearest_neighbors)
		print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))

		print ("Step.2 - Similarity score calculation - Finished ")
		# Writes the 'named_nearest_neighbors' to a json file
		with open(settings.jsons_path, 'w') as out:
				json.dump(named_nearest_neighbors, out)
		print ("Step.3 - Data stored in 'nearest_neighbors.json' file ")
		print("--- Prosess completed in %.2f minutes ---------" %
		((time.time() - start_time)/60))
		product_index = named_nearest_neighbors[1]['image_index']
		return products[product_index]