'''
Module to create the crime priorites list that organizes all the beats by their overall priority
'''

from Priority_CAN import *
from Heap_sort_CAN import *

def create_crime_priority_list(file_name):
    crime_objs = crime_priorities(file_name)
    loc_objs = location_priorities(file_name)

    file = open(file_name, 'r')
    headers = file.readline().split(',')
    lines =  file.readlines()
    beat_dict = {} # key is beat and value is an object

    # get total prioirty for each line and store the result in beat_dict
    for line in lines:
        # clean line
        line = line.strip().split(',')

        # get priority of crime that happened in the beat
        current_crime = line[5]
        current_priority = get_priority_for_crime(crime_objs, current_crime)

        # store beat and crime priority in beat_dict
        if line[10] == None or line[10] == 'false' or line[10] == 'true' or line[10] == ' LYFT)"': #Beat
            pass
        elif line[10] in beat_dict.keys():
            beat_dict[line[10]].priority += current_priority
            beat_dict[line[10]].count += 1
        else:
            beat_dict[line[10]] = location_metalist(line[10])

    # lower the priority number, higher the priority
    for beat in beat_dict:
        beat_dict[beat].priority = beat_dict[beat].priority / beat_dict[beat].count

    crime_metalist = []
    for key in beat_dict.keys():
        crime_metalist.append(beat_dict[key])

    crime_priorities_list = []

    for i in range(len(crime_metalist)):
        priority = crime_metalist[i].priority
        patrol_rectangle = 0
        for j in range(len(loc_objs)):
            if int(loc_objs[j].value) == int(crime_metalist[i].beat):
                patrol_rectangle = loc_objs[i].patrol_rectangle

        crime_priorities_list.append(metalist_obj(priority, patrol_rectangle))

    # sort the crime metalist
    crime_priorities_list = heap_sort(crime_priorities_list)

    for p in range(len(crime_priorities_list)):
        crime_priorities_list[p].key = p# rerank the priorities to start from 0 (after the heap_sort the priorities are sorted as well)

    return crime_priorities_list

def get_priority_for_crime(crime_objs, current_crime):
    for obj in crime_objs:
        if obj.value == current_crime:
            return obj.priority

class location_metalist:
    def __init__(self, beat):
        self.beat = beat
        self.count = 1
        self.priority = 0

    def __repr__(self):
        return "Beat: " + str(self.beat) + " Priority: " + str(self.priority)

class metalist_obj:
    def __init__(self, key, value):
        self.key = key # priority of the locations
        self.value = value # tuple for patroling

    def __repr__(self):
        return "Priority: " + str(self.key) + " Patrol: " + str(self.value[0]) + " " + str(self.value[1]) + " " + str(self.value[2]) + " " + str(self.value[3])
        # return "Priority: " + str(self.key)

### TEST CODE
#create_crime_priority_list("Chicago_Crimes_2018-2019_Train.csv")
