import pandas as pd
from math import radians, cos, sin, asin, sqrt

# Collect data
df = pd.read_csv('bikeracks.csv', header=1)

lat = float(input('Enter latitude: '))
lng = float(input('Enter longitude: '))

dflats = df['Latitude'].tolist()
dflngs = df['Longitude'].tolist()

# Tests whether a bike rack is closer to current location than another
# Returns distance to bike rack in miles if True and 0 if False
def closer(curr_lat, curr_lng, test_lat, test_lng, curr_dist):
    lat1 = radians(curr_lat) 
    lng1 = radians(curr_lng) 
    lat2 = radians(test_lat) 
    lng2 = radians(test_lng) 

    dlng = lng2 - lng1
    dlat = lat2 - lat1

    x = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    y = 2 * asin(sqrt(x))
    radius = 3956 # radius of the Earth in miles

    distance = y * radius
    if distance < curr_dist: return distance
    else: return 0    

# Search for the closest location and save distance, latitude, and longitude
dist = 1000
close_lat = None
close_lng = None
for x, y in zip(dflats, dflngs):
    d = closer(lat, lng, float(x), float(y), dist)
    if d:
        dist = d
        close_lat = x
        close_lng = y

# Extract information relevant to closest bike rack 
row = df.index[df['Latitude'] == close_lat].tolist()[0]
if df._get_value(row,'Longitude') != close_lng:
    print('Error: unable to locate bike rack in dataframe')
    exit()
else:
    rack_id = df._get_value(row,'RackID')
    address = df._get_value(row,'Address')
    community = df._get_value(row,'Community Name')
    if df._get_value(row,'Historical') == 1:
        historical = 'yes'
    else:
        historical = 'no'

print('\nClosest Bike Rack Found:')
print('Address:', address)
print('Distance:', '%.2f' % dist, 'miles away')
print('ID:', rack_id)
print('Neighborhood:', community)
print('Historical:', historical)
