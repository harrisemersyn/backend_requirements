from re import I
from flask import Flask, render_template , json, redirect, url_for, request, flash, session, request
from flask_wtf import FlaskForm
from datetime import datetime
import sqlite3
from csv import DictReader
import json
import os

app = Flask(__name__ , template_folder="templates", static_url_path='', static_folder="static")
app.config['SECRET_KEY'] = "placeholder"

class navlink:
  def __init__(self, title, page, to):
    self.title = title
    self.page = page
    self.to = to

navlinks = []
navlinks.append(navlink("About", "about", "/about"))
navlinks.append(navlink("Search", "search", "/search"))
navlinks.append(navlink("Rankings", "rankings", "/rankings"))

# Load the state abbreviation data
with open('states.csv', 'r') as fd:
    states_csv = DictReader(fd)
    states = {}
    for state in states_csv:
        states[state['Abbreviation']] = state['State']

class mountainToMapPage:
  def __init__(self, unique_name, name, state, statistics, trails, lifts):
    self.unique_name = unique_name
    self.name = name
    self.state = states[state]
    self.statistics = statistics
    self.trails = trails
    self.lifts = lifts

def getdbconnection():
    conn = sqlite3.connect('databases.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.jinja", nav_links = navlinks, active_page = "index")

@app.route("/about")
def about():
    return render_template("about.jinja", nav_links = navlinks, active_page = "about")

@app.route("/search")
def search():
    #parsing query string for database search
    q = request.args.get('q')
    if q:
        q = "%" + q  + "%"
    else:
        q = "%%"
    page = request.args.get('page')
    if not page:
        page = 1
    limit = request.args.get('limit')
    if not limit:
        limit = 20
    diffmin = request.args.get('diffmin')
    if not diffmin:
        diffmin = 0
    diffmax = request.args.get('diffmax')
    if not diffmax:
        diffmax = 100
    location = request.args.get('location')
    if location:
        location = "%" + location + "%"
    else:
        location = "%%"
    trailsmin = request.args.get('trailsmin')
    if not trailsmin:
        trailsmin = 0
    trailsmax = request.args.get('trailsmax')
    if not trailsmax:
        trailsmax = 1000

    page = int(page)
    limit = int(limit)
    bottomlimit = limit*(page-1)
    
    conn = getdbconnection()
    elements = len(conn.execute('SELECT mountainid FROM Mountains').fetchall())
    mountains = conn.execute('SELECT * FROM Mountains WHERE name LIKE ? AND state LIKE ? AND trail_count >= ? AND trail_count <= ? AND difficulty >= ? AND difficulty <= ? LIMIT ? OFFSET ?', (q, location, trailsmin, trailsmax, diffmin, diffmax, limit, bottomlimit)).fetchall()
    
    mountains_data = []
    for mountain in mountains:
        mountains_data.append({
            'name': mountain['name'],
            'beginner_friendliness': mountain['beginner_friendliness'],
            'difficulty': mountain['difficulty'],
            'state': states[mountain['state']],
            'trail_count': mountain['trail_count'],
            'vertical': mountain['vertical'],
            'map_link': url_for('map', mountainid = mountain['mountainid'])
        })

    conn.close()

    pages = {}
    if elements > limit & (limit * page) < elements:
        pages["next"] = "/search?q=" + q + "&page=" + str((page + 1)) + "&limit=" + str(limit) + "&diffmin=" + str(diffmin) + "&diffmax=" + str(diffmax) + "&location" + location + "&trailsmin=" + str(trailsmin) + "&trailsmax=" + str(trailsmax)
    if bottomlimit != 0:
        pages["prev"] = "/search?q=" + q + "&page=" + str((page - 1)) + "&limit=" + str(limit) + "&diffmin=" + str(diffmin) + "&diffmax=" + str(diffmax) + "&location" + location + "&trailsmin=" + str(trailsmin) + "&trailsmax=" + str(trailsmax)

    return render_template("mountains.jinja", nav_links = navlinks, active_page = "search", mountains = mountains_data, pages = pages)

@app.route("/rankings")
def rankings():
    sort = request.args.get('sort')
    if not sort:
        sort = "beginner"
    order = request.args.get('order')
    if not order: 
        order = "asc"
    #converts query string info into SQL
    conn = getdbconnection()
    if sort == "beginner":
        if order == "asc":
            mountains = conn.execute('SELECT * FROM Mountains ORDER BY beginner_friendliness ASC').fetchall()
        else: 
            mountains = conn.execute('SELECT * FROM Mountains ORDER BY beginner_friendliness DESC').fetchall()
    else:
        if order == "asc":
            mountains = conn.execute('SELECT * FROM Mountains ORDER BY difficulty ASC').fetchall()
        else:
            mountains = conn.execute('SELECT * FROM Mountains ORDER BY difficulty DESC').fetchall()
    conn.close()
    return render_template("rankings.jinja", nav_links = navlinks, active_page = "rankings", mountains = mountains, sort = sort, order = order)

@app.route("/map/<int:mountainid>")
def map(mountainid):
    conn = getdbconnection()

    mountain_row = conn.execute('SELECT name, state, trail_count, lift_count, vertical FROM Mountains WHERE mountainid = ?',(mountainid,)).fetchone()
    if not mountain_row:
        return "404"

    statistics = {
        "Trail Count": mountain_row['trail_count'],
        "Lift Count": mountain_row['lift_count'],
        "Vertical": str(mountain_row['vertical']) + 'm'
    }

    trails = conn.execute('SELECT name, difficulty FROM Trails WHERE mountainid = ?',(mountainid,)).fetchall()
    lifts = conn.execute('SELECT name FROM Lifts WHERE mountainid = ?', (mountainid,)).fetchall()
    conn.close()

    mountain = mountainToMapPage(mountainid, mountain_row['name'], mountain_row['state'], statistics, trails, lifts)

    return render_template("map.jinja", nav_links = navlinks, active_page = "map", mountain = mountain)

@app.route("/data/<int:mountainid>/objects", methods = ['GET'])
def mountaindata(mountainid):
    conn = getdbconnection()
    trailrows = conn.execute('SELECT * FROM Trails WHERE mountainid = ?', (mountainid,)).fetchall()
    liftrows = conn.execute('SELECT liftid, name FROM Lifts WHERE mountainid = ?', (mountainid,)).fetchall()
    conn.close()

    if not trailrows:
        return "404"

    trails = []
    for trail in trailrows:
        trailentry = {
            "id": trail['trailid'],
            "name": trail['name'],
            "difficulty": trail['difficulty'],
            "length": trail['length'],
            "vertical_drop": trail['vertical_drop'],
            "steepest_pitch": trail['steepest_pitch']
        }
        trails.append(trailentry)
    trailsLabeled = {
        "trails": trails
    }

    lifts = []
    for lift in liftrows:
        liftentry = {
            "id": lift['liftid'],
            "name": lift['name'],
        }
        lifts.append(liftentry)
    liftsLabeled = {
        "lifts": lifts
    }
    
    jsonContents = []
    jsonContents.append(trailsLabeled)
    jsonContents.append(liftsLabeled)
    jsonstring = json.dumps(jsonContents)
    return jsonstring

@app.route("/data/<int:mountainid>/map.svg", methods = ['GET'])
def svgmaps(mountainid):
    conn = getdbconnection()
    mountainname = conn.execute('SELECT name FROM Mountains WHERE mountainid = ?', (mountainid,)).fetchone()
    conn.close()

    if not mountainname:
        return "404"

    svgfilename = str(mountainname['name']) + ".svg"
    for filename in os.scandir('svgfiles'):
        strfilename = str(os.path.basename(filename.path))
        newstrfilename = strfilename.replace(" ", "_").lower()
        if newstrfilename == svgfilename:
            return newstrfilename
    fullfilename = "svgfiles\\" + newstrfilename
    fileContent = open(fullfilename, 'r')
    return fileContent

@app.route("/data/<int:mountainid>/paths", methods = ['GET'])
def pathdata(mountainid):
    conn = getdbconnection()
    trails = conn.execute('SELECT * FROM Trails WHERE mountainid = ?', (mountainid,)).fetchall()
    lifts = conn.execute('SELECT * FROM Lifts WHERE mountainid = ?', (mountainid,)).fetchall()
    if not trails:
        conn.close()
        return "404"
    alltrails = []
    for trail in trails:
        trailid = trail['trailid']
        tpcontents = conn.execute("SELECT latitude, longitude, elevation FROM TrailPoints WHERE trailid = ?", (trailid,))
        for tp in tpcontents:
            trailstring = str(round(tp['latitude'], 5)) + "," + str(round(tp['longitude'], 5)) + "," + str(round(tp['elevation'], 1)) + "|"
        finaltrailstring = trailstring.removesuffix("|")
        trailInput = {
            "id": trailid,
            "points": finaltrailstring
        }
        alltrails.append(trailInput)

    allifts = []
    for lift in lifts:
        liftid = lift['liftid']
        lpcontents = conn.execute("SELECT latitude, longitude, elevation FROM LiftPoints WHERE liftid = ?", (liftid,))
        for lp in lpcontents:
            liftstring = str(round(lp['latitude'], 5)) + "," + str(round(lp['longitude'], 5)) + "," + str(round(lp['elevation'], 1)) + "|"
        finalliftstring = liftstring.removesuffix("|")
        liftInput = {
            "id": liftid,
            "points": finalliftstring
        }
        allifts.append(liftInput)

    finalJSON = {
        "trails": alltrails,
        "lifts": allifts
    }

    conn.close()
    jsonstring = json.dumps(finalJSON)
    return jsonstring

if __name__ == "__main__":
    app.run()
