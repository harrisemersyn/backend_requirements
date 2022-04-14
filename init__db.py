import sqlite3, csv, csvfiles
import os

connection = sqlite3.connect('databases.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('csvfiles\mountain_list.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        todb = [(i['mountain'], i['file_name'], i['direction'], i['state'], i['difficulty'], i['ease'], i['vert'], i['trail_count'], i['lift_count']) for i in dr]
cur.executemany("INSERT INTO Mountains (name, osm_file_name, direction, state, difficulty, beginner_friendliness, vertical, trail_count, lift_count) VALUES (? , ?, ?, ?, ?, ?, ?, ?, ?);", todb)

for filename in os.scandir(r'csvfiles\trails'):
    with open(filename.path, 'r') as fin:
        dr = csv.DictReader(fin)
        mountainname = str(os.path.basename(filename.path))
        mountainname = mountainname.replace('.csv', '')
        mountainid = str(cur.execute('SELECT mountainid FROM Mountains WHERE name = ?', (mountainname,)).fetchone())
        mountainid = ''.join(x for x in mountainid if x.isdigit())
        todb = [(i['name'], i['is_area'], i['difficulty'], i['difficulty_modifier'], i['steepest_pitch'], i['vert'], i['length'], i['id'], mountainid) for i in dr]
    cur.executemany("INSERT INTO Trails (name, is_area, difficulty, difficulty_modifier, steepest_pitch, vertical_drop, length, trailid, mountainid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", todb)

for filename in os.scandir(r'csvfiles\lifts'):
    with open(filename.path, 'r') as fin:
        dr = csv.DictReader(fin)
        mountainname = str(os.path.basename(filename.path))
        mountainname = mountainname.replace('.csv', '')
        mountainid = str(cur.execute('SELECT mountainid FROM Mountains WHERE name = ?', (mountainname,)).fetchone())
        mountainid = ''.join(x for x in mountainid if x.isdigit())
        todb = [(i['name'], i['id'], mountainid) for i in dr]
    cur.executemany("INSERT INTO Lifts (name, liftid, mountainid) VALUES (?, ?, ?);", todb)

for filename in os.scandir(r'csvfiles\trail_points'):
    with open(filename.path, 'r') as fin:
        dr = csv.DictReader(fin)
        todb = [(i[''], i['trail_id'], i['for_display'], i['lat'], i['lon'], i['elevation'], i['slope']) for i in dr]
    cur.executemany("INSERT INTO TrailPoints (ind, trailid, for_display, latitude, longitude, elevation, slope) VALUES (?, ?, ?, ?, ?, ?, ?);", todb)


for filename in os.scandir(r'csvfiles\lift_points'):
    with open(filename.path, 'r') as fin:
        dr = csv.DictReader(fin)
        todb = [(i[''], i['lift_id'], i['lat'], i['lon'], i['elevation']) for i in dr]
    cur.executemany("INSERT INTO LiftPoints (ind, liftid, latitude, longitude, elevation) VALUES (?, ?, ?, ?, ?);", todb)

print("complete")
connection.commit()
connection.close()