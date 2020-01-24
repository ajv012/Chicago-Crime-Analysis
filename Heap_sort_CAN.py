'''
Module for heap sort. USes heap class
'''

from Heap_CAN import *
from random import *

def heap_sort(unsorted_list):
    # create heap
    heap = minHeap()
    # insert elements of unsorted_list into a heap
    for element in unsorted_list:
        heap.insert(element)

    # sorted_list
    sorted_list = []
    while len(heap) > 0:
        sorted_list.append(heap.extract())

    return sorted_list
