
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, text
from helpers import apology, login_required
import os

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# In this case, we are connecting to a file database called mypets.db
engine = create_engine("sqlite:///mypets.db")

# In this case, we are connecting to a cloud database
#
#
# Insert code for connecting to cloud database
#
#
#






@app.route("/")
# @login_required # This decorator is not needed as I want everybody to view the index page to be able to subscribe
def index():
    """Just renders the index page"""

    return render_template("index.html"), 200

@app.route("/newpet", methods=["POST", "GET"])
@login_required
def newpet():
    """
    This function allows the user to add a new pet to the database
    User must be logged in in order to add a new pet.
    If user not logged in, then redirected to index page
    """

    if request.method == "GET":
        return render_template("newpet.html"), 200
    else:
        petname = request.form.get("petname")
        lastname = request.form.get("lastname")
        age = request.form.get("age")
        specie = request.form.get("specie")
        id = session["user_id"]

        with engine.connect() as db:
            db.execute(text(f"INSERT INTO pets (name, lastname, age, specie, pet_id) VALUES ( '{petname}', '{lastname}', '{age}', '{specie}', '{id}')"))

        return redirect('/mypets')





@app.route("/<int:pet_num>", methods=["POST", "GET"])
@login_required
def showpet(pet_num):

    # pet_num = request.form.get("name")

    # If user want's to add a new history to the pet
    with engine.connect() as db:
        if request.method == "POST":
            db.execute("INSERT INTO history (pet_id, story, pet_num) VALUES ('{0}', '{1}', '{2}');".format(
                                session["user_id"], request.form.get("history"), pet_num))

        # If user just wants to view the pet's history
        pets = db.execute('SELECT * FROM pets WHERE pet_num = {0}'.format(pet_num)).fetchall()
        history = db.execute('SELECT * FROM history WHERE pet_num = {0}'.format(pet_num)).fetchall()

    return render_template("showpet.html", pets=pets, history=history), 200


@app.route("/deletehist/<int:histnum>", methods=["POST", "GET"])
@login_required
def deletehist(histnum):
    """
    This function allows the user to delete a history from the database.
    User must be logged in in order to delete a history.
    If user not logged in, then redirected to index page
    """

    with engine.connect() as db:
        pet_num2 = db.execute("SELECT pet_num FROM history WHERE histnum = '{0}'".format(histnum)).fetchall()
        pet_num = pet_num2[0]['pet_num']
        # print(pet_num)
        # pets = db.execute('SELECT * FROM pets WHERE pet_num = {0}'.format(pet_num))
        # history = db.execute('SELECT * FROM history WHERE {0}'.format(pet_num))
        db.execute("DELETE FROM history WHERE histnum = '{0}'".format(histnum))

    return redirect(url_for('showpet', pet_num = pet_num))
    # return redirect(f'/{pet_num}', code=200)
    #return render_template("showpet.html", pets=pets, history=history)

@app.route("/deletepet/<int:pet_num>", methods=["POST", "GET"])
@login_required
def deletepet(pet_num):
    """
    Function to delete a pet from the database
    It also deletes all the history associated with the pet
    User must be logged in in order to delete a pet.
    """
    # Connect to database & delete pet and history
    with engine.connect() as db:
        db.execute("DELETE FROM pets WHERE pet_num = '{0}'".format(pet_num))
        db.execute("DELETE FROM history WHERE pet_num = '{0}'".format(pet_num))

    return redirect("/mypets")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Function to log in a user.
    """

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
        with engine.connect() as db:
            print("-----------------------------------------", request.form.get("username"))
            username = request.form.get("username")
            rows = db.execute(text(f"SELECT * FROM users WHERE username = '{username}'")).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username or password", 403)

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



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":

        pwd = request.form.get("password")
        pwd2 = request.form.get("confirmation")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 400)
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Must provide password", 400)
        # Ensure password confirmation
        if pwd != pwd2:
            return apology("Password not the same", 400)
        
        # Ensure password has a number
        #nmbrs = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
        #if not nmbrs in pwd:
        #    return apology("Didn't put a number", 400)

        with engine.connect() as db:
            # Check if username already exists
            usr = request.form.get("username")
            rows = db.execute(text(f"SELECT * FROM users WHERE username = '{usr}'")).fetchall()

            if len(rows) == 1:
                return apology("Username already in use", 400)

            # Inserts new user
            pwd = generate_password_hash(request.form.get("password"))
            
            db.execute(f"INSERT INTO users (username, hash) VALUES ('{usr}', '{pwd}')")

        # Redirect user to home page
        return redirect("/")


@app.route("/mypets", methods=["GET", "POST"])
@login_required
def mypets():

    with engine.connect() as db:
        pets = db.execute("SELECT * FROM pets WHERE pet_id =:id", id=session["user_id"]).fetchall()
        history = db.execute("SELECT * FROM history WHERE pet_id =:id", id=session["user_id"]).fetchall()


    return render_template("mypets.html", pets=pets, history=history)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# Use to run local and make tests
# app.run(debug=True, port=8080)

# Use to dockerize
port = int(os.environ.get('PORT', 5000))
app.run(debug=True, host='0.0.0.0', port=port)