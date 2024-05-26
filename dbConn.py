import MySQLdb
# Database configuration code.
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'computing',
    'db': 'AdventureWorks2019',
}
# Create a connection to the database
conn = MySQLdb.connect(**db_config)              