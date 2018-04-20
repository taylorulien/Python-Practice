import subprocess
import os
import sys

# Argument after calling python script. Input path to folder of PBF files or single PBF file
pbfDirectory = sys.argv[1]
pbfGeoNames = []

# Creates list of PBF file or files
if pbfDirectory.endswith('.pbf'):
    filename = pbfDirectory.split('/')
    pbfDirectory = '/'.join(filename[:-1])
    pbfGeoNames.append(filename[-1])
else:
    for filename in os.listdir(pbfDirectory):
        if filename.endswith(".pbf"):
            pbfGeoNames.append(filename[:-4])

print (pbfGeoNames)

# Iterates through list of PBF files
for file in pbfGeoNames:
    db_name = ''

    # Removes characters that will break postgres
    if '.' or '-' in file:
        db_name = file.replace('.', '_')
        db_name = db_name.replace('-', '_').lower()

    print (db_name)

    # Creates Postgres DB
    process = subprocess.Popen(
        ['psql',
         '--command=DROP DATABASE IF EXISTS ' + db_name + ';',
         '--command=CREATE DATABASE ' + db_name + ';',
         '--command=\connect ' + db_name + ';',
         '--command=CREATE EXTENSION postgis;'
         ])
    process.wait()

    # Connects PBF file with Postgres DB with osm2pgsql
    connection = subprocess.Popen(
        ['osm2pgsql',
         '--create',
         '--database',
         db_name,
         '/Users/trulien/Documents/checks/pbffiles/' + file + '.pbf'])
    connection.wait()

print (">>>>>>>>>>>>>>>> SCRIPT COMPLETED <<<<<<<<<<<<<<<<<<<")
