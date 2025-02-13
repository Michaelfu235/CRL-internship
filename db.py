import sqlite3, random, datetime



#parts = [] 

#connect to sqlite3 and create database
connection = sqlite3.connect("part.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS parts (
        idd INTEGER,
        name TEXT,
        amnt INTEGER
    )
""")



connection.commit()
connection.close()

