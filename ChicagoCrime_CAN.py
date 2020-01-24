"""
Main driver for chicago crime analysis
"""

# imports
from Priority_CAN import *
from Heap_CAN import *
from AVL_tree_CAN import *
from Visualization_CAN import *
import sys
sys.setrecursionlimit(10 ** 6)
from bridges.bridges import *
from bridges.avl_tree_element import *
from Crime_priority_metalist_CAN import *

class ChicagoCrimeAnalysis:

	def __init__(self, file_name):
		"""
		Constructor that could do several things, including read in your training data
		"""
		# get the crime objects
		# each crime object has a name, count, and priority
		self.crimes_objects = crime_priorities(file_name)

		# get the location objects
		# each location object has a beat, count, and priority
		self.location_objects = location_priorities(file_name)

		# create loc_priority tree
		self.loc_object_tree = self.build_loc_priority()

		# create crime_priority tree
		self.crime_object_tree = self.build_crime_priority()

		# visualize the location_objects tree
		print('Location Priority Tree Link')
		visualize_tree(self.loc_object_tree.root, 2)

		# visualize the tree
		print('Crime Priority Tree Link')
		visualize_tree(self.crime_object_tree.root, 3)

		# declare dispatch queue
		self._dispatch_queue = minHeap()

		# creat crime_priority_list (to be used when dispatch_queue is empty and no new request made)
		self._crime_priority_list = create_crime_priority_list(file_name)

		# counter for where we are on the crime priority list
		self._crime_priority_list_counter = 0

	def build_loc_priority(self):
		"""
		Should be used to build your location-priority AVL tree
		"""
		# create a new root and use that to create a tree
		loc_priority_tree = AVLTree()

		# add all elements to the tree
		for i in range(len(self.location_objects)):

			# create new AVL Tree Element
			new_node = AVLTreeElement(self.location_objects[i].key, self.location_objects[i])

			# add color to the new node
			new_node.visualizer.color = self.get_color(new_node, 1)

			# add label to the new node
			new_node.label = 'Beat: ' + str(new_node.value.value) + "\nBeat Priority: " + str(new_node.value.priority)

			# insert the new node
			loc_priority_tree.insert_node(new_node)

		# return tree so that it can be stored in an attribute
		return loc_priority_tree

	def build_crime_priority(self):
		"""
		Should be used to build your crime-priority AVL tree
		"""
		# create a new root and use that to create a tree
		crime_priority_tree = AVLTree()

		# add all elements to the tree
		for i in range(len(self.crimes_objects)):
			# print(self.crimes_objects[i])

			# create new AVL Tree Element
			new_node = AVLTreeElement(self.crimes_objects[i].key, self.crimes_objects[i])

			# add color to the new node
			new_node.visualizer.color = self.get_color(new_node, 2)

			# add label to the new node
			new_node.label = 'Crime: ' + new_node.value.value + "\nCrime Priority: " + str(new_node.value.priority)

			# insert the new node
			crime_priority_tree.insert_node(new_node)

		# return tree so that it can be stored in an attribute
		return crime_priority_tree

	def get_dispatch_queue(self):
		return self._dispatch_queue

	def get_crime_priority_list(self):
		return self._crime_priority_list

	def add_dispatch(self, priority = -1 ,dispatch_string=''):
		'''
		Method to add a dispatch to our dispatch_queue
		Parameters:
			dispatch_string: [string] A string that represents a recent 911 dispatch call request that is reported to the police
		'''
		# assert valid dispatch string
		assert dispatch_string is not None, "Invalid dispatch string"

		# convert the dispatch string to list so that you can access the data
		dispatch_str = str(dispatch_string)
		dispatch_list = dispatch_str.split(',')

		if priority == -1:
			# get the priority of the crime based on crime and locations
			crime = dispatch_list[5].strip()
			crime_based_priority = self.crime_object_tree.get_priority(crime)
			beat = int(dispatch_list[10].strip())
			location_based_priority = self.loc_object_tree.get_priority(beat)

			total_priority = crime_based_priority + location_based_priority
		else:
			total_priority = priority

		new_node = AVLTreeElement(total_priority, dispatch_string)
		new_node.label = "Overall Priority " + str(new_node.key)
		self._dispatch_queue.insert(new_node)

	def decide_next_patrol(self, new_request=None):
		"""
		You will need this later, but I'm just giving this here for you to keep it as a placeholder
		new_request format: "ID, Case, Number, Date, Block, IUCR, Primary, Type, Description,
		Location Description, Arrest, Domestic, Beat, District, Ward, Community, Area, FBI Code, X Coordinate, Y Coordinate, Updated On, Latitude, Longitude"
		return tuple of four tuples --> rectangle for patroling
		"""
		# this variable will become a tuple that holds four tuples that define a rectangle to patrol
		patrol_rectangle = 0

		if new_request is not None:
			# if a new request is coming in, then we want to send a patrol to that location immediately!
			# do preprocessing on the string to get it into a useable format
			new_request_list = new_request.split(',')
			# get the crime latitide and longitude from the file
			crime_lat =  float(new_request_list[21].strip())
			crime_long = float(new_request_list[22].strip())
			# set the patrol tuples
			patrol_rectangle = self.get_rectangle(crime_lat, crime_long)

		elif len(self._dispatch_queue) > 0:
			# dispatch_queue is not empty and no new request made, so extract from dispatch queue
			dispatch = self._dispatch_queue.extract().value.strip().split(',')

			# get the latitude and longitude of the location of crime
			lati = dispatch[len(dispatch) - 3]
			long = dispatch[len(dispatch) - 2]
			# if the file does not provide the latitude and longitude we set it to a default coordinate
			if lati == '':
				lati = 41.8781
				long = -87.6298
			else:
				lati = float(lati)
				long = float(long)
			# set the patrol tuples
			patrol_rectangle = self.get_rectangle(lati, long)

		else:
			# dispatch queue is empty and no new request is made so use crime_priority_list to send new patrol
			index = self._crime_priority_list_counter % len(self._crime_priority_list)
			# set the patrol tuples
			patrol_rectangle = self._crime_priority_list[index].value
			self._crime_priority_list_counter += 1

		return str(patrol_rectangle)


	def get_color(self, node, tree):
		"""
		Assigns a color to the visual tree node based on the priority. More red = Higher priority, Lighter/ More green = Lower priority
		tree = 1 --> loc_priority_tree
		tree = 2 --> crime_priority_tree
		"""
		p = int(node.value.priority)
		if tree == 1:
			if p >= 0 and p <= 50:
				return 'red'
			elif p >= 51 and p <= 100:
				return 'lightcoral'
			elif p >= 101 and p <= 150:
				return 'orangered'
			elif p >= 151 and p <= 200:
				return 'darkgoldenrod'
			elif p >= 201 and p <= 250:
				return 'lime'
			else:
				return 'royalblue'
		elif tree == 2:
			if p >= 0 and p <= 4:
				return 'red'
			elif p >= 5 and p <= 9:
				return 'lightcoral'
			elif p >= 10 and p <= 14:
				return 'orangered'
			elif p >= 15 and p <= 19:
				return 'darkgoldenrod'
			elif p >= 20 and p <= 24:
				return 'lime'
			elif p >= 25 and p <=29:
				return 'royalblue'
			else:
				return 'turquoise'

	def get_rectangle(self, latitude, longitude):
		'''
		1 deg of longitude or latitude is 69.2 miles, so rectangle coordinates change by 0.1 deg (rectangle has an area of 49 square miles)
		'''
		top_left = (latitude + 0.1, longitude - 0.1)
		top_right = (latitude + 0.1, longitude + 0.1)
		bottom_right = (latitude - 0.1, longitude + 0.1)
		bottom_left = (latitude - 0.1, longitude - 0.1)
		rectangle = (top_left, top_right, bottom_right, bottom_left)
		return rectangle

c = ChicagoCrimeAnalysis('Chicago_Crimes_2018-2019_Train.csv')
