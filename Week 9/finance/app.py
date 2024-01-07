import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""


    user_id = session["user_id"]

    # Get info about the stocks the user owns
    rows = db.execute("SELECT symbol, SUM(shares) as shares, price FROM purchases WHERE user_id = ? GROUP BY symbol", user_id)

    # Get the amount of money the user has
    cash = float((db.execute("SELECT cash FROM users WHERE id = ?", user_id))[0]["cash"])
    cash_total = cash

    # For every stock owned
    for row in rows:
        # Get current price
        current_price = float((lookup(row["symbol"]))["price"])

        # Set price as current price
        row["price"] = current_price
        # Capitalize the sumbol
        row["symbol"] = (row["symbol"]).upper()
        # Create and set total as price * number of shares
        row["total"] = float(current_price) * float(row["shares"])

        # Add to total
        cash_total += row["total"]

        # Convert total and price to USD format
        row["total"] = usd(row["total"])
        row["price"] = usd(row["price"])

    return render_template("index.html", info=rows, total=usd(cash_total), cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        try:
            # Making sure user has inputted symbol
            symbol = request.form.get("symbol")

            if not symbol:
                return apology("Please enter a stock symbol!")

            # Making sure the user has inputted shares in a valid way
            shares = int(request.form.get("shares"))

            if not shares:
                return apology("Please enter shares")

            if shares <= 0:
                return apology("Shares must be grateer than zero")

            # Looking up price and buying stock

            stock = lookup(symbol)

            if not stock:
                return apology("Stock does not exist")

            # Get user ID, calculate the price of stock and check if user has enough cash to buy it
            user_id = session["user_id"]
            price = stock["price"] * shares
            user_cash = ((db.execute("SELECT cash FROM users WHERE id = ?", user_id))[0]["cash"])

            if price > user_cash:
                return apology("You do not have enough cash!")

            # Deduct cash from user
            db.execute("UPDATE users SET cash = ? WHERE id = ?", (user_cash - price), user_id)

            # Make a record of their purchase
            time = datetime.now()

            db.execute("INSERT INTO purchases (user_id, symbol, shares, price, time) VALUES(?, ?, ?, ?, ?)", user_id, symbol, shares, stock["price"], time)

            # Congratulate them :33
            flash("STOCK PURCHSED!!!!")

            return redirect("/")
        except ValueError:
            return apology("You can only buy an integer number of stocks")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]

    rows = db.execute("SELECT * FROM purchases WHERE user_id = ? ORDER BY time DESC", user_id)

    for row in rows:
        row["symbol"] = (row["symbol"]).upper()
        row["price"] = usd(row["price"])

        if row["shares"] < 0:

            row["type"] = "Sold"
            row["shares"] = row["shares"] * -1

        else:
            row["type"] = "Brought"


    return render_template("history.html", info=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
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
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Come on... You need to give me a symbol")

        stock = lookup(symbol)

        if not stock:
            return apology(f'No stock with symbol"{symbol}" found!')

        return render_template("quoted.html", symbol= stock["symbol"], price= usd(stock["price"]))

    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")
        conf_password = request.form.get("confirmation")

        # Submission validation
        if not user:
            return apology("Username is required")

        elif not password:
            return apology("Must enter password!")

        elif not conf_password:
            return apology("Must confirm password!")

        # Make sure username is not taken
        others = db.execute("SELECT * FROM users WHERE username = ?", user)

        if len(others) != 0:
            return apology("Username is already taken!")

        # Make sure passwords match
        elif password != conf_password:
            return apology("The passwords must match!")

        else:
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", user, generate_password_hash(password))
            return redirect(url_for("login"))

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Getting and validating the symbol and shares
        # Symbols
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("You did not select the stock symbol")

        # shares
        shares = request.form.get("shares")

        if not shares:
            return apology("You did not enter the number of shares :(")

        shares = int(shares)

        if shares <= 0:
            return apology("Shares must be greater than 0!!")

        # Seeing if user has enough of the stock
        user_id = session["user_id"]

        info = db.execute('SELECT symbol, SUM(shares) as shares FROM purchases WHERE user_id = ? AND symbol = ? GROUP BY symbol', user_id, symbol)

        if len(info) == 0:
            return apology(f"You do not own any {(info[0]['symbol']).upper()} stock!")

        if info[0]["shares"] < shares:
            return apology(f"You do not have {shares} shares of this stock!")

        # Get the cash the user has
        cash = float((db.execute("SELECT cash FROM users WHERE id = ?", user_id))[0]["cash"])
        # Get price of the stock
        current_price = lookup(symbol)["price"]
        # Get total value of stocks the user wanst to sell
        total = current_price * shares
        # Get updated cash value
        new_cash = cash + total
        # Update the user's cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)

        # Make record of the purchase
        time = datetime.now()
        # value of share is negative to differenciate between buying and selling
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price, time) VALUES(?, ?, ?, ?, ?)", user_id, symbol, (shares * -1), total , time)

        flash(f"STOCK SOLDDD!!! FOR {usd(total)}")

        return redirect("/")

    else:
        user_id = session["user_id"]
        # Get stock symbols and render thme
        stocks = db.execute("SELECT symbol FROM purchases WHERE user_id = ? GROUP BY symbol", user_id)

        symbols = [stock["symbol"] for stock in stocks]

        return render_template("sell.html", symbols=symbols)



@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def change():
    '''Allows user to change password'''
    if request.method == "POST":
        # Validate submissoins
        # old password
        old = request.form.get("old")
        if not old:
            return apology("Old password is a must")

        # New password
        new = request.form.get("password")
        if not new:
            return apology("Enter the password dummy :/")

        # password confirmation
        confirm = request.form.get("confirmation")
        if not confirm:
            return apology("Come one... confirm your password...")

        user_id = session["user_id"]
        # Chech if user typed old password correctly
        old_hash = (db.execute("SELECT hash FROM users WHERE id = ?", user_id))[0]["hash"]

        if generate_password_hash(new) != old_hash:
            return apology("The old password is wrong!")


        # Chack if passwords match
        if confirm != new:
            return apology("The new password and confirmation must match!")

        # Update the password
        new_hash = generate_password_hash(new)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

        flash("Password changed")
        return redirect("/")

    else:
        return render_template("password.html")


