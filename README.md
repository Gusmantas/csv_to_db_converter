# CSV-to-Database Converter
This is a simple application used to convert a .csv file to local database.
Simply, import a file with a single button, preview its content, give a name to to-be-converted
database, hit "Convert" button and set a location for your new database file. 
Databases generated with this tool can be used as regular databases
for programming.

NOTE!

Foreign keys are not added after converting, and must be placed manually. 
This tool also adds an index column to database, even if .csv file have it, so make sure to review
database before using it.
To open database file use a database management tool, such as SQLite Studio, HeidiSQL or other. 

This application was built using Python with these libraries:
* TKinter
* Pandas
* SQLAlchemy

