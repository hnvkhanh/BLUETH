import os, csv, random


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)    
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

def sort_func(d):
    return d["point"]

#Sort list of cards by point
@app.template_filter('sort')
def filter_shuffle(seq):
    try:
        result = list(seq)
        result.sort(key=sort_func)
        return result
    except:
        return seq

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if (request.form.get("fluency")):
        response = request.form.get("fluency")
        fluency = response[0]
        response = response[1:]
        card_id = int(response)
        card_point = db.execute("SELECT point FROM cards WHERE id = ?", card_id)
        if fluency == "g":
            db.execute("UPDATE cards SET point = ? WHERE id = ?", card_point[0]["point"] + 2, card_id)
        elif fluency == "f":
            db.execute("UPDATE cards SET point = ? WHERE id = ?", -1, card_id )
        else:
            db.execute("UPDATE cards SET point = ? WHERE id = ?", card_point[0]["point"] + 1, card_id)
        return ("",204)
    if (request.form.get("deleted-card")):
        db.execute("DELETE FROM cards WHERE id = ?", request.form.get("deleted-card"))
    cards = db.execute("SELECT * FROM cards WHERE user_id = ?", session.get("user_id"))
    number_of_cards = len(cards)
    return render_template("index.html", CARDS=cards, length=number_of_cards)

    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("login.html", alert = 1)
        elif not request.form.get("password"):
            return render_template("login.html", alert = 2)
        rows = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", alert = 3)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")
        
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return render_template("register.html", alert = 1)
        rows = db.execute("SELECT name FROM users WHERE name = ?", username)
        if len(rows) != 0:
            return render_template("register.html", alert = 4)
        password = request.form.get("password")
        if not password:
            return render_template("register.html", alert = 2)
        if password != request.form.get("confirmation"):
            return render_template("register.html", alert = 3)
        db.execute("INSERT INTO users (name, hash) VALUES(?, ?)", username, generate_password_hash(password))
        rows = db.execute("SELECT * FROM users WHERE name = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/") 
    else:
        return render_template("register.html")


@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    langs = [];
    filename = "language.csv"
    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            langs.append(row)
    if request.method == "GET":
        return render_template("add.html", LANGS = langs)
    else:
        word = request.form.get("word")
        if not word:
            return render_template("add.html", alert = 1, LANGS = langs)
        types = request.form.get("type")
        if not types:
            return render_template("add.html", alert = 2, LANGS = langs)
        meaning = request.form.get("meaning")
        if not meaning:
            return render_template("add.html", alert = 3, LANGS = langs)
        example = request.form.get("example")
        note = request.form.get("note")
        db.execute("INSERT INTO cards (user_id, word, type, meaning, example, note) VALUES(?,?,?,?,?,?)", session.get("user_id"), word, types, meaning, example,note)
        return render_template("add.html", LANGS = langs)
    
@app.route("/setting", methods=["GET", "POST"])
@login_required
def setting():
    if request.method == "POST":
        if (request.form.get("reset")):
            db.execute("DELETE FROM cards WHERE user_id = ?", session.get("user_id"))
        if (request.form.get("delete")):
            db.execute("DELETE FROM cards WHERE user_id = ?", session.get("user_id"))
            db.execute("DELETE FROM users WHERE id = ?", session.get("user_id"))
            return redirect("/logout")
        if (request.form.get("password") and request.form.get("save")):
            new_pass = request.form.get("password")
            confirm = request.form.get("confirm")
            if new_pass != confirm:
                return render_template("setting.html", alert = 1)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_pass), session.get("user_id"))
        if (request.form.get("name")):
            new_name = request.form.get("name")
            db.execute("UPDATE users SET name = ? WHERE id = ?", new_name, session.get("user_id"))
    return render_template("setting.html")
        
    
        
