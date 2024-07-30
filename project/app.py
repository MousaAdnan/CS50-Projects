import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# Routes
@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect("/login")
    user_id = session["user_id"]
    notes = Note.query.filter_by(user_id=user_id).all()
    return render_template("index.html", notes=notes)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password, method="sha256")
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")

@app.route("/note/new", methods=["GET", "POST"])
def new_note():
    if not session.get("user_id"):
        return redirect("/login")
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        new_note = Note(title=title, content=content, user_id=session["user_id"])
        db.session.add(new_note)
        db.session.commit()
        return redirect("/")
    return render_template("new_note.html")

@app.route("/note/<int:note_id>")
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != session.get("user_id"):
        return redirect("/")
    return render_template("view_note.html", note=note)

@app.route("/note/<int:note_id>/edit", methods=["GET", "POST"])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != session.get("user_id"):
        return redirect("/")
    if request.method == "POST":
        note.title = request.form.get("title")
        note.content = request.form.get("content")
        db.session.commit()
        return redirect(f"/note/{note_id}")
    return render_template("edit_note.html", note=note)

@app.route("/note/<int:note_id>/delete")
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != session.get("user_id"):
        return redirect("/")
    db.session.delete(note)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
