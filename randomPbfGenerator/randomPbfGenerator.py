import random
import csv
import requests
import json
import time
import os

'''
The purpose of this script is to produce a list of 7 random countries (one per region) and request a pbf file with
predefined bounding boxes from https://export.hotosm.org:

Author: Taylor
'''

config = json.loads(open('config.json').read())

def RandomCountrySelector():
    countries = dict()
    results = list()
    output = dict()

    # Read csv file and create dictionary with keys as regions and values as different countries
    with open('./input/countryList.csv') as myFile:
        reader = csv.DictReader(myFile)
        for row in reader:
            if row['continents'] not in countries:
                countries[row['continents']] = [row['country']]
            else:
                countries.setdefault(row['continents'], []).append(row['country'])

    # Randomly select country from each region
    for key, value in countries.items():
        results.append(random.choice(value))

    # List of selected countries
    print("Countries randomly selected: ", results)

    # Attach attributes from seperate csv file to selected countries
    with open('./input/cityBoundingBox.csv') as myFile:
        reader = csv.reader(myFile)

        for row in reader:
            for country in results:
                if row[0] == country:
                    output[country] = [row[1], row[2], row[3], row[4], row[5]]
    return output

def HOTExportAPI ():
    # Run RandomCountrySelector function
    output = RandomCountrySelector()
    # Grab variables from config
    hotExportUrl = config["HOTExportURL"]
    hotExportAPIToken = config["HOTExportToken"]

    # Iterate through each country in dictionary. Will create pbf.zip file for each country in downloads folder in current directory
    for key, value in output.items():
        country = key
        city = value[0]
        west = float(value[1])
        south = float(value[2])
        east = float(value[3])
        north = float(value[4])
        name = city + '-' + country

        # JSON information to send to HotExport
        values = {
            'published': 'false',
            'feature_selection': 'buildings:\n    types:\n        - lines\n        - polygons\n    select:\n        - name\n        - building\n    where: building IS NOT NULL',
            'export_formats': ['bundle'],
            'name': name,
            'description': 'description',
            'event': 'event',
            'aoi': {
                'description': 'Draw',
                'geomType': 'Polygon',
                'title': 'Custom Polygon'
            },
            'the_geom': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [west, north],
                        [west, south],
                        [east, south],
                        [east, north],
                        [west, north]
                    ]
                ]
            }
        }

        # Send HTTP POST Request to HotExport and receive UID. Job is being processed
        requestHeaders = {"Authorization": "Bearer " + hotExportAPIToken, "Content-Type": "application/json"}
        request = requests.post(hotExportUrl + "/api/jobs", data=json.dumps(values), headers=requestHeaders)
        response = request.json()

        id = response["uid"]
        print("Downloading " + name + "...")

        # Ping HotExport until job status is COMPLETED. Save file to ***downloads folder in current directory***
        while True:
            request = requests.get(hotExportUrl + '/api/runs?job_uid=' + id)
            response = request.json()

            status = response[0]["status"]
            print('Status of ' + name + 'is: ' + status)

            if status == "COMPLETED":
                # get download url from response
                download_url = response[0]["tasks"][0]["download_urls"][0]["download_url"]
                dir_path = os.path.dirname(os.path.realpath(__file__))

                # download pbf to local directory
                downloadReponse = requests.get(hotExportUrl + '/' + download_url, stream=True)
                handle = open(dir_path + '/downloads/' + name + '.bundle.tar.gz', 'wb')
                for chunk in downloadReponse.iter_content(chunk_size=512):
                    if chunk:
                        handle.write(chunk)

                # Print elapsed time for process
                elapsed_time = response[0]["elapsed_time"]
                print("Time elapsed for " + name + ", " + elapsed_time + ' seconds')

                break
            elif status == "FAILED":
                print (name + " failed.")

                # Print elapsed time for process
                # elapsed_time = info2[0]["elapsed_time"]
                # print ("Time elapsed for " + name + ", " + elapsed_time + ' seconds')
                break
            else:
                time.sleep(10)    # Ping HotExport every 10 seconds
                continue

HOTExportAPI()
print ("SCRIPT COMPLETED")
