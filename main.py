from re import I
from flask import Flask, render_template , json, redirect, url_for, request, flash, session, request
from flask_wtf import FlaskForm
from datetime import datetime
import sqlite3
from csv import DictReader

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

    elements = len(mountains)
    pages = []
    if elements > limit:
        next = (url_for('/search', page = page + 1))
        pages.append(next)
    if bottomlimit != 0:
        prev = (url_for('/search', page = page - 1))
        pages.append(prev)

    return render_template("mountains.jinja", nav_links = navlinks, active_page = "search", mountains = mountains_data, pages = pages)

@app.route("/nextpage")
def nextpage():
    return redirect()

@app.route("/rankings")
def rankings():
    sort = request.args.get('sort')
    order = request.args.get('order')
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
    mountain = conn.execute('SELECT * FROM Mountains WHERE mountainid = ?',(mountainid,)).fetchone()
    trails = conn.execute('SELECT * FROM Trails WHERE mountainid = ?',(mountainid,)).fetchall()
    lifts = conn.execute('SELECT * FROM Lifts WHERE mountainid = ?', (mountainid,)).fetchall()
    conn.close()

    return render_template("map.jinja", nav_links = navlinks, active_page = "map", mountain = mountain, trails = trails, lifts = lifts)

if __name__ == "__main__":
    app.run()
