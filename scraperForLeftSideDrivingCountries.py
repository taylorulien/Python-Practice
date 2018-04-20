from bs4 import BeautifulSoup
import requests
import csv

# Call LeftHandDrivingCountries wiki page and read page
LeftHandDrivingCountries = requests.get("https://en.wikipedia.org/wiki/List_of_countries_with_left-hand_traffic")
data = LeftHandDrivingCountries.text
soup = BeautifulSoup(data, "html.parser")
driveLeft = []

# scrape URL page
for one in soup.find_all('ul'):
    for two in one.find_all('a'):
        value = (two.get('title'))

        if value is not None:
            driveLeft.append(value)

# Remove non-country names
output = driveLeft[:(driveLeft.index('Seychelles'))]

# write csv file
with open('leftSideDriving.csv', 'w') as myFile:
    writer = csv.writer(myFile)
    writer.writerow(output)
