import sqlite3

connection = sqlite3.connect('databases.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO Mountains (osmfilename, name, location, direction, trailcount, liftcount, vertical, difficulty, beginnerfriendliness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('andes.osm', 'Andes Tower Hills', 'Minnesota', 'N', 12, 2, 5.24, 3.0, 1.0)
            )
cur.execute("INSERT INTO Mountains (osmfilename, name, location, direction, trailcount, liftcount, vertical, difficulty, beginnerfriendliness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('andes.osm', 'Andes Tower Hills', 'Minnesota', 'N', 15, 6, 6.74, 5.0, 2.0)
            )

connection.commit()
connection.close()