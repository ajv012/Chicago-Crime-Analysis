'''
Module to crerate an AVL tree and critical methods for AVL tree such as
inserting and removing and balancing the AVL tree
'''

class AVLTree:
	def __init__(self):
		"""
		Constructor for AVL Tree class
		"""
		self.root = None

	def insert_node(self, node):
		if self.root is None:
			# first node is none, so set it as the root
			self.root = node
		else:
			# call insert method to properly insert node and balance tree
			self.root = self._insert_node(self.root, node)

	def _insert_node(self, root, node):
		"""
		Insert method for inserting nodes in the AVL and balancing the tree
		Some parts of this method were inspired from the algorithm present on the website: https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
		"""
		# create a normal BST before you start balancing the tree
		if root is None:

			# you have reached the end of the tree so insert the node
			return node

		elif node.key < root.key:

			# since new key is smaller than the parent, go to the left
			root.left = self._insert_node(root.left, node)

			# increase height, which is the max of right and left subtrees
			root.height = max(self._get_height(root.left)+1, self._get_height(root.right))

		elif node.key > root.key:

			# since new key is larger than the parent, go to the right
			root.right = self._insert_node(root.right, node)

			# increase height, which is the max of right and left subtrees
			root.height = max(self._get_height(root.left), self._get_height(root.right)+1)

		# code hereon is called after recursion
		# get the balance factor for the node
		balance = self._get_balance(root)

		if balance > 1 and node.key < root.left.key:

			# case 1, so roatate right
			root = self._right_rotate(root)

		elif balance < -1 and node.key > root.right.key:

			# case 3, so rotate left
			return self._left_rotate(root)

		elif balance > 1 and node.key > root.left.key:

			# case 2, so rotate left and then rotate right
			root.left = self._left_rotate(root.left)
			return self._right_rotate(root)

		elif balance < -1 and node.key < root.right.key:

			# Case 4, so rotate right and then rotate left
			root.right = self._right_rotate(root.right)
			return self._left_rotate(root)

		# return root
		return root

	def _right_rotate(self, parent):
		# copy nodes
		child = parent.left
		grandchild = child.right

		# rotate right
		child.right = parent
		parent.left = grandchild

		# update heights
		parent.height = max(self._get_height(parent.left), self._get_height(parent.right)) + 1
		child.height = max(self._get_height(child.left), self._get_height(child.right)) + 1

		return child  # return the child node

	def _left_rotate(self, parent):
		# copy nodes
		child = parent.right
		grandchild = child.left

		# rotate
		child.left = parent
		parent.right = grandchild

		# update heights
		parent.height = max(self._get_height(parent.left), self._get_height(parent.right)) + 1
		child.height = max(self._get_height(child.left), self._get_height(child.right)) + 1

		return child  # return the child node

	def _get_height(self, root):
		# if at the end, then return -1 (thanks Prof. Dancy!)
		if root is None:
			return -1
		# else return the actual height
		return root.height

	def _get_balance(self, root):
		# if root is none then just return 0
		if root is None:
			return 0
		else:
			# balance factor is just te different between the heights
			return self._get_height(root.left) - self._get_height(root.right)

	def preorder(self):
		return self._preorder(self.root)

	def _preorder(self, node):

		# perform a preorder on the tree
		if node is not None:
			print(str(node.key) + ' height: ' + str(node.height))
			self._preorder(node.left)
			self._preorder(node.right)

	def get_priority(self, target):
		return self._get_priority(self.root, target)

	def _get_priority(self, node, target):
		'''
		returns the priority associated with the key. Each node is AVLTreeElement (key = count of crime or beat, value is crime or location object)
		'''
		# this priority variable will be returned
		priority = -1
		if node is not None:
			if str(target).isdigit():# if it takes in the beat
				if node.value.key == target:
					return node.value.priority
			else:
				if node.value.value == target:
					return node.value.priority
				priority = self._get_priority(node.left, target)
				if priority == -1:
					priority = self._get_priority(node.right, target)
		return priority
