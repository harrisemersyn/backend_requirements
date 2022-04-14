import sqlite3, csv, csvfiles
import os

connection = sqlite3.connect('databases.db')

#with open('schema.sql') as f:
    #connection.executescript(f.read())

cur = connection.cursor()

with open("\csvfiles\mountainlist.csv", 'r') as fin:
        dr = csv.DictReader(fin)

for csv in "\csvfiles":
    with open(csv, 'r') as fin:
        dr = csv.DictReader(fin)
        todb = [(i['name'], i['trailid'], i['is_area'], i['difficulty'], i['difficulty_modidier'], i['steepest_pitch'], i['vert'], i['length']) for i in dr]
    mountainname = os.path.splitext(csv)
    mountainid = cur.execute('SELECT mountainid FROM Mountains WHERE name = ?', (mountainname,)).fetchone()
    cur.executemany("INSERT INTO Trails (name, trailid, is_area, difficulty, difficulty_modifier, steepest_pitch, vertical_drop, length, mountainid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, mountainid);", todb)

connection.commit()
connection.close()