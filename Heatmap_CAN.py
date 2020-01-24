'''
Module for creating heat map
'''

from gmplot import gmplot
# import gmaps

def get_coords(filename = 'Chicago_Crimes_2018-2019_Train.csv'):
    file = open(filename, 'r')
    headers = file.readline().split(',')
    files =  file.readlines()
    lati_list = []
    long_list = []
    for line in files:
        line = line.strip().split(',')
        lati = line[len(line) - 2]
        long = line[len(line) - 1]
        # print(lati, long)
        if lati == '':
            lati = 41.8781
            long = -87.6298
        else:
            lati = lati[2:len(lati)]
            long = long[1:(len(long)-2)]
        lati_list.append(float(lati))
        long_list.append(float(long))
        # print(float(lati), float(long))
    return lati_list, long_list

# def create_heatmap(coords):
#     gmap = gmplot.GoogleMapPlotter.from_geocode("Chicago")
#     #gmap.heatmap(coords)
#     gmap.figure()

# def main():
#     locations_list = get_coords()
#     create_heatmap(locations_list)


def main():
    # gmap.heatmap(int(41.922724629), int(-87.769594212))
    # locations_list = get_coords()
    # create_heatmap(locations_list)
    latitudes, longitudes = get_coords()
    # gmap = gmplot.GoogleMapPlotter.from_geocode("Chicago")
    gmap = gmplot.GoogleMapPlotter(41.8781, -87.6298, 11)
    gmap.heatmap(latitudes, longitudes)
    # gmap.apikey = 'AIzaSyB9-qRNhrCwGu8vAbWy4z8aUdwS8dapmN4'
    gmap.draw('heatmap_CAN.html')

# def main():
#     locations = get_coords()
#     gmaps.configure(api_key='AIzaSyAaQh7SEytpuqPdDznGaU6UmbZNXk1M15o')
#     fig = gmaps.figure(map_type='HYBRID')
#     heatmap_layer = gmaps.heatmap_layer(locations)
#     fig.add_layer(heatmap_layer)
#     fig

main()
