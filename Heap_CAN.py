'''
Heap class with critical methods such as insert and extract
'''

from math import log

class minHeap:
    def __init__(self):
        self._heap_list = []
        self._size = 0
        self._level = 0

    def __len__(self):
        return self._size

    def get_level(self):
        return self._level

    def get_heap(self):
        return self._heap_list

    def __str__(self):
        '''
        Print the Heap inorderly
        '''
        s = ''
        for i in self._heap_list:
            s += str(i) + ' '
        return s

    def is_empty(self):
        return self._size == 0

    def _switch(self, ind_1, ind_2):
        '''
        Swap two nodes with each other
        '''
        temp = self._heap_list[ind_1]
        self._heap_list[ind_1] = self._heap_list[ind_2]
        self._heap_list[ind_2] = temp

    def insert(self, AVLTreeElement):
        '''
        Insert a AVLTreeElement into the Heap then re-order the Heap if needed
        '''
        self._heap_list.append(AVLTreeElement)
        # increase the size
        self._size += 1
        # get the index of the newly added AVLTreeElement
        cur_ind = self._size - 1
        # recalculate the level
        self._level = round(log(cur_ind+1, 2))

        if self._size == 2 and self._heap_list[1].key < self._heap_list[0].key:
            self._switch(0,1)
        else:
            # get the index of the parent of that new AVLTreeElement
            if cur_ind % 2 == 0:
                parent_ind = cur_ind//2 - 1
            else:
                parent_ind = cur_ind//2# example: 5//2 = 2
            # check shift-up logic
            while self._heap_list[parent_ind].key > self._heap_list[cur_ind].key:
                self._switch(parent_ind, cur_ind)
                # update the index
                cur_ind = parent_ind
                if cur_ind == 0:
                    break
                if cur_ind % 2 == 0:
                    parent_ind = cur_ind//2 - 1
                else:
                    parent_ind = cur_ind//2

    def extract(self):
        '''
        Extracts the root of Heap and then re-order it
        '''
        assert self._size > 0, 'cannot pop an empty heap bro'

        if len(self._heap_list) == 1:
            self._size = self._size - 1
            item_to_return = self._heap_list[0]
            self._heap_list.remove(item_to_return)
            return item_to_return
        elif len(self._heap_list) == 2:
            self._size = self._size - 1
            item_to_return = self._heap_list[0]
            self._heap_list.remove(item_to_return)
            return item_to_return
        else:
            self._size = self._size - 1
            item_to_return = self._heap_list[0]

            # remove the item
            self._heap_list.remove(item_to_return)

            # remove last item
            last_item = self._heap_list.pop()

            # insert last item at the start
            self._heap_list.insert(0, last_item)

            # do the sift down logic
            i = 0

            while (2*i + 1) <= len(self._heap_list) - 1:
                parent = self._heap_list[i]
                # left child always present
                left_child = self._heap_list[2*i + 1]

                # right child may not be present
                if 2*i + 2 <= len(self._heap_list) - 1:
                    right_child = self._heap_list[2*i + 2]
                else:
                    right_child = None

                if right_child is not None:
                    if parent.key > min(left_child.key, right_child.key):
                        # switch required, find the switch
                        if left_child.key < right_child.key:
                            self._switch(i, 2*i + 1)
                        else:
                            self._switch(i, 2*i + 2)
                else:
                    # right child is not present
                    if parent.key > left_child.key:
                        self._switch(i, 2*i + 1)
                i = i + 1

            return item_to_return

    def peek(self, index):
        assert index > 0 and index < len(self._heap_list), "Can't peek here baby"

        return self._heap_list[index]


### TEST CODE
# class Node:
#     def __init__(self, key, value):
#         self.key = key
#         self.value = value
#
#     def __repr__(self):
#         return str(self.key)

# h = minHeap()
# h.insert(Node(12, "2"))
# h.insert(Node(8, "2"))
# h.insert(Node(5, "2"))
# h.insert(Node(11, "2"))
# h.insert(Node(7, "2"))
# h.insert(Node(4, "2"))
# h.insert(Node(9, "2"))
# h.insert(Node(2, "2"))
# h.insert(Node(10, "2"))
# print(h.extract())
# print(h.extract())
# print(h.extract())
# print(h.extract())
# print(h.extract())
# print(h.extract())
# print(h.extract())
# print(h.extract())
# print(h.extract())
# print(h.get_heap())
