from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, get_tone
from datetime import datetime

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
@login_required
def index():
    '''
    show all entry titles, time, tone and ability to remmove them
    '''


@app.route("/add" , methods=["GET", "POST"])
@login_required
def add():
    '''Add new entry'''


@app.route("/remove", methods=["POST"])
@login_required
def remove():
    '''Remove an entry'''


@app.route("/login", methods=["GET", "POST"])
def login():
    '''Log user in'''


@app.route("/register", methods=["GET" ,"POST"])
def register():
    '''Allow user to register with username and password'''


@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def change():
    '''Allow user to change password'''