'''
Module for assging priorities to crimes and locations
'''

class Crime:

    # in trees, the crime object will be the key and we will use the count attribute for the comparisons
    # in trees, the priority attribute will be the priority or value of the tree node

    def __init__(self, name, UID):
        self.value = name
        self.key = UID
        self.count = 0
        self.priority_divisions = 0
        self.priority_frequency = 0
        self.priority_arrest_rate = 0
        self.priority = 0

    # count the overall priority base on the divisions, frequency and arrest rate
    def set_priority(self):
        self.priority = round(0.6*self.priority_divisions + 0.2*self.priority_frequency + 0.2*self.priority_arrest_rate,2)

    # set priority frequency
    def set_f_prior(self, p):
        self.priority_frequency = p

    # set priorit devisions
    def set_d_prior(self, p):
        self.priority_divisions = p

    def set_a_prior(self, p):
        self.priority_arrest_rate = p

    def __repr__(self):
        return "Name: " + self.value + " UID: " + str(self.key) + " Overall crime prior: " + str(self.priority)

    def __gt__(self, other):
        return self.key > other.key

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return self.key == other.key

def sort_crime_dict(crime_dict):

    # create List
    crime_list = [] #List of Crime objects
    for i in crime_dict:
        crime_list.append(crime_dict[i])

    # bubble sort the crime list
    for i in range(len(crime_list)):
        for j in range(len(crime_list) - i - 1):
            if crime_list[j].count < crime_list[j+1].count:
                crime_list[j], crime_list[j+1] = crime_list[j+1], crime_list[j]

    # assign frequency based priorty
    for f in range(len(crime_list)):
        crime_list[f].set_f_prior(f)

    return crime_list

def assign_divisional_priority(crime_list):
    # crime divisions as set by Dallas city public safety department
    priority_0_division = ['WEAPONS VIOLATION', 'INTERFERENCE WITH PUBLIC OFFICER', 'KIDNAPPING'] # under 8 minutes response
    priority_1_division = ['BATTERY', 'CRIMINAL DAMAGE', 'ASSAULT','ROBBERY', 'HOMICIDE', 'ARSON'] #under 12 minutes response
    priority_2_division = ['CRIM SEXUAL ASSAULT' , 'NARCOTICS','LIQUOR LAW VIOLATION', 'CONCEALED CARRY LICENSE VIOLATION' , 'PUBLIC INDECENCY', 'PUBLIC PEACE VIOLATION'] #under 30 minutes response
    priority_3_division = ['OFFENSE INVOLVING CHILDREN',  'SEX OFFENSE', 'MOTOR VEHICLE THEFT' , 'THEFT',  'BURGLARY' , 'CRIMINAL TRESPASS', 'STALKING' , 'INTIMIDATION', 'HUMAN TRAFFICKING', 'PROSTITUTION', 'OBSCENITY'] # under 60 minutes response
    priority_4_division = ['DECEPTIVE PRACTICE',  'OTHER OFFENSE' , 'GAMBLING', 'OTHER NARCOTIC VIOLATION', 'NON-CRIMINAL', 'NON-CRIMINAL (SUBJECT SPECIFIED)'] # on telephone

    for crime in crime_list:
        if crime.value in priority_0_division:
            crime.set_d_prior(0)
        elif crime.value in priority_1_division:
            crime.set_d_prior(8)
        elif crime.value in priority_2_division:
            crime.set_d_prior(16)
        elif crime.value in priority_3_division:
            crime.set_d_prior(24)
        elif crime.value in priority_4_division:
            crime.set_d_prior(32)

def assign_arrest_rate_priority(crime_list):
    for crime in crime_list:
        if crime.value in ['INTERFERENCE WITH PUBLIC OFFICER', 'THEFT', 'PUBLIC PEACE VIOLATION']:
            crime.set_a_prior(0)
        elif crime.value == 'HOMICIDE':
            crime.set_a_prior(8)
        elif crime.value == 'CRIM SEXUAL ASSAULT':
            crime.set_a_prior(16)
        elif crime.value in ['CRIMINAL DAMAGE', 'BURGLARY']:
            crime.set_a_prior(24)
        else:
            crime.set_a_prior(32)

# reassign the final priority
def assign_final_crime_priority(crime_list):
    for crime in crime_list:
        crime.set_priority()

def sort_crime_list(crime_list):
    crime_list_new = [i for i in crime_list]

    # bubble sort the crime list
    for i in range(len(crime_list_new)):
        for j in range(len(crime_list_new) - i - 1):
            if crime_list_new[j].priority > crime_list_new[j+1].priority:
                crime_list_new[j], crime_list_new[j+1] = crime_list_new[j+1], crime_list_new[j]

    return crime_list_new

def set_user_friendly_priorirty(list):
    # renumber priorities so that priority is more user friendly (starts from 0, 1, 2, ...)
    for i in range(len(list)):
        list[i].priority = i

def crime_priorities(file_name):
    '''
    For each crime in the dataset, assigns priority based on three factors:
    1. 5 crime divisions created by Dallas city Public Safety Committee (60%)
    2. Priority based on frequency of the crime (20%)
    3. Priority based on average arrest rate/crime (20%)
    Total priorty is the sum of priorities 1, 2 and 3. Total priority out of 100
    Lower number is higher priority
    '''

    #find frequency of each crime
    file = open(file_name, 'r')
    headers = file.readline().split(',')
    files =  file.readlines()
    crime_count = {}
    count = 0

    # create the crime dict dictionary where key is primary type of crime and value is the frequency
    for line in files:
        line = line.strip().split(',')
        if line[5] in crime_count.keys(): #'Primary Type' of the crime
            crime_count[line[5]].count += 1
        else:
            crime_count[line[5]] = Crime(line[5], count)
            count = count + 1

    # sort dictionary based on crime frequency
    crime_list_sorted = sort_crime_dict(crime_count)

    # assign divisional priority
    assign_divisional_priority(crime_list_sorted)

    # assign higher priority to crimes that disproportionately affect different races
    # crimes: murder, drug crimes, sexual assault
    # crimes: interference with public officers, homicide, crim sexual assault, sex offense, theft, burglary, deceptive practice
    assign_arrest_rate_priority(crime_list_sorted)

    # assign final prioirty
    assign_final_crime_priority(crime_list_sorted)

    # sort crime list once more based on priorty
    crime_priority_list = sort_crime_list(crime_list_sorted)

    # make priority user firendly
    set_user_friendly_priorirty(crime_priority_list)

    return crime_priority_list

class Location:

    def __init__(self, beat, UID):
        self.value = beat # count
        self.key = UID
        self.crime_count = 1
        self.priority = 0.0
        self.crime_weight = 0.0 # keeps tracks of what crimes are happening in the beat
        self.normalized_crime_priority = 0.0
        self.patrol_rectangle = 0.0
        self.community_priority = 100

    # count the overall priority base on the crime weight, crime count and community priority
    def set_priority(self):
        self.normalized_crime_priority = self.crime_weight / self.crime_count
        self.priority = 0.7*self.normalized_crime_priority + 0.3*self.community_priority

    # set community priority
    def set_community_priority(self, p):
        self.community_priority = p

    def __repr__(self):
        return "Beat: " + str(self.value) + " Count: " + str(self.crime_count) + " Priority: " + str(self.priority)

    def __gt__(self, other):
        return self.key > other.key

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return self.key == other.key

    # set the patrol to a tuple
    def set_patrol_rectangle(self, patrol_rectangle_tuple):
        self.patrol_rectangle = patrol_rectangle_tuple

def create_location_list(location_dict, crime_location_dict):
    location_list = []

    for beat in location_dict:
        location_dict[beat].set_patrol_rectangle(crime_location_dict[beat])
        location_list.append(location_dict[beat])

    return location_list

def sort_location_list(location_list):
    location_list_new = [i for i in location_list]

    #Sort location_list
    for i in range(len(location_list_new)):
        for j in range(len(location_list_new) - i - 1):
            if location_list_new[j].priority > location_list_new[j+1].priority:
                location_list_new[j], location_list_new[j+1] = location_list_new[j+1], location_list_new[j]

    return location_list_new

def beats_in_comunity_areas(file_name):
    # code to put beats in their community areas
    file = open('Chicago_Crimes_2018-2019_Train.csv', 'r')
    headers = file.readline().split(',')
    files =  file.readlines()
    area = {} # keys are community areas, value is list of beats in Community

    for line in files:
        line = line.strip().split(',')
        if line[10] == None or line[10] == 'false' or line[10] == 'true' or line[10] == ' LYFT)"' or line[13] == "" or line[13] == " " or line[13] == '0' or line[13] == 'true' or line[13] == ' LYFT)"':
            pass
        elif line[13] in area.keys():
            if line[10] not in area[line[13]]:
                area[line[13]].append(line[10])
        else:
            area[line[13]] = []
            area[line[13]].append(line[10])

    return area

def set_community_area_priority(location_list, beats_and_communityAreas):
    # define community areas
    community_0_priority = [26, 27, 29, 37, 38, 40, 67, 68, 69, 42, 43, 54, 53, 73,49,44,47,48,45,71 ] # most black
    community_1_priority = [50, 25,36,]
    community_2_priority = [51, 75, 46, 35, 39, 66]
    community_3_priority = [1, 72, 28, 61, 70,41, 33, 23 ]
    community_4_priority = [2, 77, 3, 8, 32, 30]
    community_5_priority = [55, 52,74,76, 9, 10, 11, 12, 13, 14, 4, 17, 15, 16,5,6,7,21,22,20,19,18,24,31,59,60,56,57,58,62,63,64,65] # least black

    for loc in location_list:

        # find beat code
        temp_communityArea_code = 0
        for code in beats_and_communityAreas:
            if loc.value in beats_and_communityAreas[code]:
                temp_communityArea_code = code
                temp_communityArea_code = int(temp_communityArea_code)

        # once you have the code, add the priority
        if temp_communityArea_code in community_0_priority:
            loc.set_community_priority(8)
        elif temp_communityArea_code in community_1_priority:
            loc.set_community_priority(8.5)
        elif temp_communityArea_code in community_2_priority:
            loc.set_community_priority(9)
        elif temp_communityArea_code in community_3_priority:
            loc.set_community_priority(9.5)
        elif temp_communityArea_code in community_4_priority:
            loc.set_community_priority(10)
        elif temp_communityArea_code in community_5_priority:
            loc.set_community_priority(10.5)
        else:
            loc.set_community_priority(11)

def location_priorities(file_name):
    '''
    Priooirty of location is decided in two layers
    1. Crime-weighted and count normalized
    2. Areas with more likelihood of false arrests
    '''

    file = open(file_name, 'r')
    headers = file.readline().split(',')
    files =  file.readlines()
    location_dict = {}
    crime_location_dict = {}
    crime_priority_list = crime_priorities("Chicago_Crimes_2018-2019_Train.csv")
    #print(crime_priority_list)
    count = 0

    # set priorty based on freqeuncy
    for line in files:
        line = line.strip().split(',')
        if line[10] == None or line[10] == 'false' or line[10] == 'true' or line[10] == ' LYFT)"': #Beat
            pass
        elif line[10] in location_dict.keys():
            # increase crime count
            location_dict[line[10]].crime_count += 1

            # increase crime weight
            temp_crime_weight = 0
            for crime in crime_priority_list:
                if line[5] == crime.value:
                    temp_crime_weight = crime.priority

            location_dict[line[10]].crime_weight += temp_crime_weight

            # crime location
            crime_location_dict[line[10]].append([line[19], line[20]])
        else:
            location_dict[line[10]] = Location(line[10], count)
            count = count + 1
            # increase crime weight
            temp_crime_weight = 0
            for crime in crime_priority_list:
                if line[5] == crime.value:
                    temp_crime_weight = crime.priority

            location_dict[line[10]].crime_weight += temp_crime_weight
            crime_location_dict[line[10]] = [[line[19], line[20]]]

    location_list = create_location_list(location_dict, crime_location_dict)


    # find what community areas do the beats belong to
    codes = beats_in_comunity_areas(file_name)

    # set priorty based on community area
    set_community_area_priority(location_list, codes)

    # Set priority of each locations
    for loc in location_list:
        loc.set_priority()

    # sort the list
    location_list_sorted = sort_location_list(location_list)


    # find average coordinates and rectangle for patroling
    for key in crime_location_dict:
        curr_list = crime_location_dict[key]
        lat_sum = 0
        long_sum = 0
        count = 0

        for i in range(len(curr_list)):
            if str(curr_list[i][0]) == "" or str(curr_list[i][0]) == " ":
                lat_sum = lat_sum + 41.881832
                long_sum = long_sum + (-87.623177)
            else:
                lat_sum = lat_sum + float(curr_list[i][0])
                long_sum = long_sum + float(curr_list[i][1])
            count = count + 1

        # reset the average latitude and longitude
        avg_lat = lat_sum / count
        avg_long = long_sum / count

        top_left = (avg_lat + 0.1, avg_long - 0.1)
        top_right = (avg_lat + 0.1, avg_long + 0.1)
        bottom_right = (avg_lat - 0.1, avg_long + 0.1)
        bottom_left = (avg_lat - 0.1, avg_long - 0.1)
        rectangle = (top_left, top_right, bottom_right, bottom_left)

        crime_location_dict[key] = rectangle

    for beat in crime_location_dict:
        for loc in location_list_sorted:
            if loc.value == beat:
                loc.set_patrol_rectangle(crime_location_dict[beat])

    # make priority user firendly
    set_user_friendly_priorirty(location_list_sorted)

    return location_list_sorted

### TEST CODE
# crime_priorities("Chicago_Crimes_2018-2019_Train.csv")
# location_priorities("Chicago_Crimes_2018-2019_Train.csv")
