import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Configure custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    stocks = db.execute("SELECT symbol, SUM(shares) as shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["total"] = stock["shares"] * stock["price"]
    total_value = cash + sum(stock["total"] for stock in stocks)
    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or password != confirmation:
            return apology("must provide valid username and matching passwords")
        hash = generate_password_hash(password)
        result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        if not result:
            return apology("username taken")
        session["user_id"] = result
        return redirect("/")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return apology("invalid username or password")
        session["user_id"] = user[0]["id"]
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")
        return render_template("quoted.html", quote=quote)
    return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide valid symbol and positive shares")
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")
        price = quote["price"]
        total_cost = int(shares) * price
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if cash < total_cost:
            return apology("not enough cash")
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, shares, price)
        return redirect("/")
    return render_template("buy.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        current_shares = db.execute("SELECT SUM(shares) as shares FROM transactions WHERE user_id = ? AND symbol = ?",
                                    session["user_id"], symbol)[0]["shares"]
        if not symbol or shares <= 0 or shares > current_shares:
            return apology("invalid transaction")
        quote = lookup(symbol)
        sale_value = shares * quote["price"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, -shares, quote["price"])
        return redirect("/")
    symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    return render_template("sell.html", symbols=symbols)

@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ?",
                              session["user_id"])
    return render_template("history.html", transactions=transactions)
