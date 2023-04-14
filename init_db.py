import csv
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

file = open('all_legs.csv')
 
contents = csv.reader(file)

insert_records = "INSERT INTO legs (mode, origin_latitude, origin_longitude, destination_latitude, destination_longitude, route_name) VALUES(?, ?, ?, ?, ?, ?)"

cur.executemany(insert_records, contents)
 
select_all = "SELECT * FROM legs"
rows = cur.execute(select_all).fetchall()

connection.commit()
connection.close()

