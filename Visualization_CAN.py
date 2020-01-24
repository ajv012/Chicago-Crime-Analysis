'''
Module to create visualizations using the bridges API
'''

from bridges.bridges import *
from bridges.avl_tree_element import *
from math import log
from Heap_CAN import *

def visualize_tree(root, key):
	"""
	Use the Bridges API to visuaize the tree
	"""

	# use login credentials to set up bridges object
	bridges = Bridges(key, "ajv012", "721329632140")

	# set up title of the tree
	bridges.set_title("AVL Tree. Color is an indicator of priority.")

	# visualize_tree_tree
	bridges.set_data_structure(root)
	bridges.visualize()

def visualize_heap(heap, key):
    '''
    input is a heap object
    output is a bridges link that visualizes the heap
	key must be larger than 1
    '''

    parent_indices = []
	#get the list of the heap
    heap_list = heap.get_heap()

    for j in range(heap.get_level()):
        parent_indices.append((2**j) - 1)

    for i in parent_indices:
		# get the parents position of the current index
        if 2*i + 1 <= len(heap)//2 - 1:
            current_parents = heap_list[i:2*i + 1]
        else:
            current_parents = heap_list[i:len(heap)//2]
		# get the left node and right node of the parent index
        for parent in current_parents:
            children = heap_list[2*heap_list.index(parent) + 1: 2*heap_list.index(parent) + 3 ]
            parent.left = children[0]
            if len(children) == 2:
                parent.right = children[1]
            else:
                parent.left = children[0]
			# recount the height
            parent.height = round(log(heap_list.index(parent)+1, 2))

    # use login credentials to set up bridges object
    bridges = Bridges(key, "ajv012", "721329632140")


    # set up title of the tree
    bridges.set_title("Dispatch Queue MinHeap")

    # set up title of the tree
    bridges.set_title("AVL Tree structure used to visualize heap.")

    # visualize
    if len(heap) > 0:
        bridges.set_data_structure(heap_list[0])
        bridges.visualize()
