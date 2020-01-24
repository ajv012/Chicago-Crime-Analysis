'''
Module that finds the arrest rates per indcidence of crime in all the community areas in Chicago. Change the name of the crime (line 26)
to see the outcome for different crimes
'''

class Beat:
    def __init__(self, beat):
        self.beat = beat
        self.arrest_count = 0
        self.crime_count = 1

    def calc_average(self):
        # set the avarage number of arrests per crime
        return self.arrest_count / self.crime_count

    def __str__(self):
        return "Community Area Code: " + str(self.beat) + " Average arrests per crime: " + str(round(100*self.calc_average(), 2))


file = open('Chicago_Crimes_2018-2019_Train.csv', 'r')
headers = file.readline().split(',')
files =  file.readlines()
location_dict = {} # key is beat number

for line in files:
    line = line.strip().split(',')
    if line[13] == None or line[13] == 'false' or line[13] == 'true' or line[13] == ' LYFT)"' or line[13] == " ": #Beat
        pass
    elif line[5] == 'THEFT':# if the crime is THEFT we proceed our logic
        if line[13] in location_dict.keys():
            location_dict[line[13]].crime_count += 1
            if line[8] == 'true':
                location_dict[line[13]].arrest_count += 1
        else:
            location_dict[line[13]] = Beat(line[13])
            if line[8] == 'true':
                location_dict[line[13]].arrest_count += 1

write_file = open('Average_Arrest_Rates_community.txt','w')
for key in location_dict:
    write_file.write(str(location_dict[key]))
    write_file.write('\n')

write_file.close()
