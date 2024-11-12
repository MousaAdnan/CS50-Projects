import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL
from datetime import datetime

# Connect to your database
db = SQL("sqlite:///book_club_hub.db")

# Execute the query to list all tables
tables = db.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Print the list of tables
print("Tables in the database:", tables)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"
Session(app)



db = SQL("sqlite:///book_club_hub.db")

app.config["TEMPLATES_AUTO_RELOAD"] = True

def apology(message):
    return render_template("apology.html", message=message)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/profile")
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("must provide username and password")
        if password != confirmation:
            return apology("passwords must match")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username already taken")

        hash_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", username, hash_password)

        flash("Registered successfully! Please log in.")
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("must provide username and password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            return apology("invalid username and/or password")

        session["user_id"] = rows[0]["id"]
        flash("Logged in successfully!")
        return redirect("/profile")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    user_info = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    books = db.execute("SELECT * FROM user_books JOIN books ON user_books.book_id = books.id WHERE user_id = ?", user_id)

    goal_progress = db.execute("SELECT COUNT(*) AS total_books FROM user_books WHERE user_id = ?", user_id)[0]["total_books"]

    return render_template("profile.html", user_info=user_info[0], books=books, goal_progress=goal_progress)

@app.route("/library", methods=["GET", "POST"])
def library():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    books = db.execute("SELECT * FROM user_books JOIN books ON user_books.book_id = books.id WHERE user_id = ?", user_id)
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        pages = request.form.get("pages")

        book = db.execute("SELECT * FROM books WHERE title = ? AND author = ?", title, author)
        if not book:
            db.execute("INSERT INTO books (title, author, genre) VALUES (?, ?, ?)", title, author, genre)
            book = db.execute("SELECT * FROM books WHERE title = ? AND author = ?", title, author)

        book_id = book[0]["id"]
        db.execute("INSERT INTO user_books (user_id, book_id, goal_pages) VALUES (?, ?, ?)", user_id, book_id, pages)

        flash(f"Added '{title}' to your library!")
        return redirect("/library")

    return render_template("library.html", books=books)

@app.route("/review_book", methods=["POST"])
def review_book():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    book_id = request.form.get("book_id")
    rating = int(request.form.get("rating"))
    review = request.form.get("review")

    db.execute("INSERT INTO reviews (user_id, book_id, rating, review) VALUES (?, ?, ?, ?)", user_id, book_id, rating, review)
    flash("Review added successfully!")
    return redirect("/library")

@app.route("/book_clubs")
def book_clubs():
    if "user_id" not in session:
        return redirect("/login")

    clubs = db.execute("SELECT * FROM book_clubs")
    return render_template("book_clubs.html", clubs=clubs)

@app.route("/club/<int:club_id>", methods=["GET", "POST"])
def club(club_id):
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        post = request.form.get("post")
        user_id = session["user_id"]
        db.execute("INSERT INTO club_discussions (club_id, user_id, post) VALUES (?, ?, ?)", club_id, user_id, post)
        flash("Post added to discussion!")

    club_info = db.execute("SELECT * FROM book_clubs WHERE id = ?", club_id)
    members = db.execute("SELECT users.username FROM club_members JOIN users ON club_members.user_id = users.id WHERE club_id = ?", club_id)
    discussions = db.execute("SELECT users.username, club_discussions.post, club_discussions.timestamp FROM club_discussions JOIN users ON club_discussions.user_id = users.id WHERE club_id = ? ORDER BY timestamp DESC", club_id)

    return render_template("club.html", club=club_info[0], members=members, discussions=discussions)

if __name__ == "__main__":
    app.run(debug=True)
