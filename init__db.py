import sqlite3

connection = sqlite3.connect('databases.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO Mountains (osm_file_name, name, state, direction, trail_count, lift_count, vertical, difficulty, beginner_friendliness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('andes.osm', 'Andes Tower Hills', 'Minnesota', 'N', 12, 2, 5.24, 3.0, 1.0)
            )
cur.execute("INSERT INTO Mountains (osm_file_name, name, state, direction, trail_count, lift_count, vertical, difficulty, beginner_friendliness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('cannon.osm', 'Cannon', 'New Hampshire', 'W', 15, 6, 6.74, 5.0, 2.0)
            )

connection.commit()
connection.close()