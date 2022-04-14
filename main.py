from re import I
from flask import Flask, render_template , json, redirect, url_for, request, flash, session, request
from flask_wtf import FlaskForm
from datetime import datetime
import sqlite3

app = Flask(__name__ , template_folder="templates")
app.config['SECRET_KEY'] = "placeholder"

def getdbconnection():
    conn = sqlite3.connect('databases.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.jinja", nav_links = "", active_page = "index")

@app.route("/about")
def about():
    return render_template("about.jinja", nav_links = "", active_page = "about")

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

    bottomlimit = limit*(page-1)
    
    conn = getdbconnection()
    
    mountains = conn.execute('SELECT * FROM Mountains WHERE name LIKE ? AND state LIKE ? AND trail_count >= ? AND trail_count <= ? AND difficulty >= ? AND difficulty <= ? LIMIT ? OFFSET ?', (q, location, trailsmin, trailsmax, diffmin, diffmax, limit, bottomlimit)).fetchall()
    conn.close()
    #TODO gets the previous page and the next page (if it exists)

    #TODO make a set of map links based off mountain ids

    return render_template("mountains.jinja", nav_links = "", active_page = "search", mountains = mountains, pages = "")

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
    return render_template("rankings.jinja", nav_links = "", active_page = "rankings", mountains = mountains, sort = sort, order = order)

@app.route("/map/<int:mountainid>/<string:name>")
def map(mountainid, name):
    conn = getdbconnection()
    mountain = conn.execute('SELECT * FROM Mountains WHERE mountainid = ?',(mountainid,)).fetchone()
    trails = conn.execute('SELECT * FROM Trails WHERE mountainid = ?',(mountainid,)).fetchall()
    lifts = conn.execute('SELECT * FROM Lifts WHERE mountainid = ?', (mountainid,)).fetchall()
    conn.close()
    return render_template("map.jinja", nav_links = "", active_page = "map", mountain = mountain, trails = trails, lifts = lifts)