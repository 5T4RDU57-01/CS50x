from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, get_tone, apology, give_message
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
    if request.method() == "GET":
        return render_template("add.html")
    
    # Get the entry and the title
    title = request.form.get("title")
    entry = request.form.get("entry")

    # Give apology for no entry
    if not entry:
        give_message("Come on, Write something :(", 'error', 'add')
    # set title to the time if not specified
    if not title:
        title = datetime.now()

    # Get userid, tone and time
    user_id = session["user_id"]
    tone = get_tone(entry)
    entry_time = datetime.now()

    # Add info to the database
    db.execute("INSERT INTO entries (user_id, title, time, entry, tone) VALUES (?, ?, ?, ?, ?)", user_id, 
                                                                                                title, 
                                                                                                entry_time, 
                                                                                                entry, 
                                                                                                tone) 
    
    # Inform user of success and redirect to index page
    give_message("Entry added!", 'message', '/')


@app.route("/remove/<str:entry_id>")
@login_required
def remove(entry_id):
    '''Remove an entry'''
    db.execute("DELETE FROM entries WHERE entry_id = ?", entry_id)
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''Log user in'''
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET" ,"POST"])
def register():
    '''Allow user to register with username and password'''
    if request.method() == "GET":
        return render_template("register.html")
    
    # Getting everything from the form
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # Validating everything
    if not username:
        give_message("Please provide a username!", 'error', '/register')
    if not password:
        give_message("Please provide a password!", 'error', '/register')
    if not confirmation:
        give_message("Please confirm your password!", 'error', '/register')


    # Seeing if Passwords match    
    if password != confirmation:
        return apology("The two passwords mush match")
    
    # Seeing if the username is already taken
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    if len(rows) != 0:
        return apology("Username is already taken!")

    # If everything checks out, register the user
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
    return redirect(url_for("login"))


@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def change():
    '''Allow user to change password'''
    if request.method() == "GET":
        return render_template("change_pass.html")

    # Get old and new passwords and password confirmation    
    old_pass = request.form.get("old")
    new_pass = request.form.get("new")
    confirmation = request.form.get("confirmation")

    # Make sure user entered all of them
    if not old_pass:
        give_message("Please enter your old password!", 'error', 'change_pass')
    if not new_pass:
        give_message("Please enter your new password!", 'error', 'change_pass')
    if not confirmation:
        give_message("Please confirm your password!", 'error', 'change_pass')
        
    # See if the two passwords match
    if new_pass != confirmation:
        give_message("The two passwords must match!", 'error', 'change_pass')

    
    # Getting the orignal password hash 
    # And hashing the old password the user gave
    user_id = session["user_id"]
    orignal_pass_hash = (db.execute("SELECT hash FROM users WHERE id = ?", user_id))[0]["hash"]
    old_pass_hash = generate_password_hash(old_pass)

    # If user messes up old password
    if check_password_hash(old_pass_hash, orignal_pass_hash) == False:
        give_message("The old password is incorrect!", 'error', 'change_pass')

    # Updating the hash and redirecting to index
    db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_pass), user_id)
    give_message("Password updated!", 'message', '/')
