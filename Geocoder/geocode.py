import urllib
import json
import csv

"""
PYTHON 2.7
"""

api = 'https://maps.googleapis.com/maps/api/geocode/json?'

# Load authentication.json file to pull the Google Geocode API KEY into file.
# Make an authentication.json file and pull a google geocode api key from: https://developers.google.com/maps/documentation/geocoding/get-api-key
apikeys = json.loads(open('../RandomCountrySelector/authentication.json').read())
key = apikeys["GoogleGeocoderKEY"]

# cities_list.csv is in the same directory
# If you want to add cities to be added to the analysis, add them into the file with its country
listcities = open('cities_list.csv', 'r')
lines = listcities.readlines()
myFields = ['country', 'city', 'W', 'S', 'E', 'N', 'FileSize_bytes']

# Loops through cities
# If it doesnt already exist in citiesouput it will push it to the geocoder API and add it to that file
for line in lines:
    loops = False

    line = line.rstrip()
    x = line.split(",")

    with open('citiesoutput.csv') as input:
        reader = csv.DictReader(input)

        for row in reader:
            if x[0] == row['city']:
                loops = True
                break
            else:
                continue

    if loops is True:
        continue
    else:
        url = api + urllib.urlencode({'sensor' : 'false', 'address' : line}) + '&key=' + key
        urlread = urllib.urlopen(url)
        data = urlread.read()
        js = json.loads(str(data))

        if js['status'] == 'ZERO_RESULTS':
            print "Not able to geocode", x[0]
            continue

        north = js["results"][0]["geometry"]["viewport"]["northeast"]["lat"]
        east = js["results"][0]["geometry"]["viewport"]["northeast"]["lng"]
        south = js["results"][0]["geometry"]["viewport"]["southwest"]["lat"]
        west = js["results"][0]["geometry"]["viewport"]["southwest"]["lng"]

        print "Adding", x[0]
        with open('citiesoutput.csv', 'a') as output:
            writer = csv.DictWriter(output, fieldnames=myFields)
            writer.writerow({'country': x[1], 'city': x[0], 'W': west, 'S': south, 'E': east, 'N': north, 'FileSize_bytes': 0})

print "SCRIPT COMPLETED"