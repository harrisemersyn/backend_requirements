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
    return render_template("rankings.jinja", nav_links = "", active_page = "rankings", mountains = "", sort = sort, order = order)

@app.route("/map/<string:mountain_name>")
def map(mountain_name):
    #check to see if active page is what's wanted
    return render_template("map.jinja", nav_links = "", active_page = "map" + mountain_name, mountain = mountain_name, trails = "", lifts = "")