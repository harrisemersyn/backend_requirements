from re import ASCII
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
    page = request.args.get('page')
    limit = request.args.get('limit')
    filters = request.args.get('filters')
    conn = getdbconnection()
    #TODO needs to use limit and filters
    mountains = conn.execute('SELECT * FROM Mountains').fetchall()
    conn.close()
    #TODO gets the previous page and the next page (if it exists)

    #TODO make a set of map links based off mountain ids

    return render_template("mountains.jinja", nav_links = "", active_page = "search", mountains = mountains, pages = "")

@app.route("/rankings")
def rankings():
    sort = request.args.get('sort')
    order = request.args.get('order')
    #converts query string info into variables readable by SQL
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