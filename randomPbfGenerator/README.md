#  Random PBF Generator

The purpose of this script is to produce a list of 7 random countries (one per region) and request a pbf file with
predefined bounding boxes from https://export.hotosm.org


the install python requirements
```python
sudo pip install requirements.txt
```


*YOU MUST PUT A BEARER TOKEN FROM HOT EXPORT TOOL INTO* config.json file in current directory ***

To get token:
    a. log into HOT Export Tool -->
    b. open up developer tools in chrome -->
    c. once logged in push on the Create tab in the website -->
    d. in develper tools click on 'Network' and you'll see a 'configuratoins?...' request with an authorization header -->
    e. The KEY is "Bearer ....." --> place it into the config.json file

 1. Loop through a list of countries in ../BoundingBoxGeocoder/countryList.csv
 2. Randomly select 1 country from each region
 3. Fetch bounding box from ../BoundingBoxGeocoder/cityBoundingBox.csv
 4. Start process of collecting pbf files from https://export.hotosm.org
 5. Send HTTP POST request to https://export.hotosm.org/api/jobs.
 6. Store response; particularly the uid
 7. Use that uid in the following HTTP GET request https://export.hotosm.org/api/runs?job_uid=[insert uid here]
 8. Continuously ping https://export.hotosm.org/api/runs?job_uid=[insert uid here] until the response[0].status = "COMPLETED"
 9. Recieve download url and download pbf.zip files to downloads folder in current directory
 10. Iterate the same request/ response with https://export.hotosm.org for all 7 countries
