from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, get_tone, apology, give_message
import datetime
from collections import Counter

# Configure application
app = Flask(__name__, static_url_path="/static")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


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
    if request.method == "GET":
        user_id = session["user_id"]
        entries = db.execute("SELECT * FROM entries WHERE user_id = ?;", user_id)
        entries = list(reversed(entries))
        return render_template("index.html", entries=entries)


@app.route("/add" , methods=["GET", "POST"])
@login_required
def add():
    '''Add new entry'''
    if request.method == "GET":
        return render_template("add.html")
    
    # Get the entry and the title
    else:
        title = request.form.get("title")
        entry = request.form.get("entry")

        # Give apology for no entry
        if not entry:
            give_message("Come on, Write something :(", 'error', 'add')
        # set title to the time if not specified
        if not title:
            title = datetime.datetime.now()

        if len(str(title)) > 150:
            title = title[0:150]

        # Get userid, tone and time
        user_id = session["user_id"]
        tone = get_tone(entry)
        entry_time = datetime.datetime.now()

        # Add info to the database
        db.execute("INSERT INTO entries (user_id, title, time, entry, tone) VALUES (?, ?, ?, ?, ?)",
                    user_id, 
                    title, 
                    entry_time, 
                    entry, 
                    tone) 
        
        # Inform user of success and redirect to index page
        flash("Entry added!", 'message')
        return redirect("/")


@app.route("/remove/<string:entry_id>")
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
    if request.method == "GET":
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
    if request.method == "GET":
        return render_template("change_pass.html")

    # Get old and new passwords and password confirmation    
    old_pass = request.form.get("old")
    new_pass = request.form.get("new")
    confirmation = request.form.get("confirmation")

    # Make sure user entered all of them
    if not old_pass:
        flash("Please enter your old password!", 'error')
        return redirect("/change_pass")
    
    if not new_pass:
        flash("Please enter your new password!", 'error')
        return redirect("/change_pass")
    
    if not confirmation:
        flash("Please confirm your password!", 'error')
        return redirect("/change_pass")
        
    # See if the two passwords match
    if new_pass != confirmation:
        flash("The two passwords must match", 'error')
        return redirect("/change_pass")

    
    # Getting the orignal password hash 
    # And hashing the old password the user gave
    user_id = session["user_id"]
    orignal_pass_hash = (db.execute("SELECT hash FROM users WHERE id = ?", user_id))[0]["hash"]
    old_pass_hash = generate_password_hash(old_pass)

    # If user messes up old password
    if check_password_hash(old_pass_hash, orignal_pass_hash) == False:
        flash("The old password is incorrrect", 'error')
        return redirect("/change_pass")
    
    # Updating the hash and redirecting to index
    db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_pass), user_id)
    flash("Password updated!" 'message')
    return redirect("/")


@app.route("/percentages/<timeframe>")
@login_required
def percentages(timeframe):
    
    timeframe_days = {
        "past_week" : 7,
        "past_month" : 30,
        "past_six_months" : 183,
        "past_year" : 365,
    }

    # Check if we somehow got a bad timeframe
    if timeframe not in timeframe_days.keys():
        timeframe = "all_time"

    # Get user id and tones of all entries associated with that user
    user_id = 1
    rows = db.execute("SELECT tone,time FROM ENTRIES WHERE user_id = ? ", user_id)

    # Get all the tones
    if timeframe == "all_time":
        tones_info = [tones["tone"] for tones in rows]

    else:
    # Get todays date and the date when the timeframe ends
        today = datetime.date.today()
        days = timeframe_days[timeframe]
        end_timeframe = today - datetime.timedelta(days=days)

        # All the entry tones if they were created after the timeframe
        
        # The abomonation after the if statement basically takes the
        # YYYY-MM-DD part of the date and converts it to a date object before comparison
        tones_info = [tones["tone"] for tones in rows if (datetime.datetime.strptime(tones["time"].split()[0], "%Y-%m-%d")).date()  >= end_timeframe]

    # Get total no of tones and the occourance of each tone
    total = len(tones_info)
    counts = Counter(tones_info)

    # Clone the counts dict
    tone_percentages = counts.copy()

    # Replace the counts with rounded percentages
    for tone in counts:
        tone_percentages[tone] = round(counts[tone] / total * 100)

    # Make the current choice look pretty
    current_choice = timeframe.replace("_", " ").title()

    return render_template("percentages.html", tone_percentages=tone_percentages, counts=counts, current_choice=current_choice, total=total)
    