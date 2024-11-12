import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
    # Fetch user's stocks
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
                        session["user_id"])

    # Get user's cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Initialize total portfolio value with user's cash balance
    total_value = cash

    # Add stock details to each stock in the portfolio
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        total_value += stock["value"]

    # Pass data to template
    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value)



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Get and validate form inputs
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol:
            return apology("provide symbol")
        elif not shares.isdigit() or int(shares) <= 0:
            return apology("needs to be positive")

        # Look up the symbol to get the price
        quote = lookup(symbol)
        if quote is None:
            return apology("symbol not found")

        # Calculate total cost
        price = quote["price"]
        total_cost = int(shares) * price

        # Fetch user's cash balance from the users table
        user_data = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if not user_data:
            return apology("user not found")

        cash = user_data[0]["cash"]

        # Ensure sufficient funds
        if cash < total_cost:
            return apology("not enough cash")

        # Update user's cash and add transaction
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, shares, price)

        # Confirm purchase and redirect to portfolio
        flash(f"Bought {shares} shares of {symbol} for {usd(total_cost)}!")
        return redirect("/")
    else:
        return render_template("buy.html")




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
        quote = lookup(symbol)
        if not quote:
            return apoology("invalid symbol", 400)
        return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Pls provide username", 400)

        elif not request.form.get("password"):
            return apology("Pls provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("Pls provide confirmation for password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 0:
            return apology("username exists", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                    request.form.get("username"), generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
