#  psqlToPostgis Script

The purpose of this script is to create a DB for a PBF file in PostgreSQL so you can run queries with PGAdmin for
analysis. You pass the script a path to a single PBF file or to a folder with multiple PBF files that you would like
to have a DB created for. *Keep in mind it will
overwrite any DB that has the same name.*


*How to run:*
1. 'cd' to the python script
2. Type the command below in terminal:
```python
python psqlToPostgis.py /PATH/TO/FILE/OR/FOLDER
```

