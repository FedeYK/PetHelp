# Importing libraries
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, text
from helpers import apology, login_required
import requests


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

# CONNECTING TO THE DATABASE

# To connect with the api 
ip_api = "https://apiph-dot-capstone-376415.oa.r.appspot.com/api/ph/v1"

# In this case, we are connecting to a cloud database
# Database Data
ip_fede = "34.175.221.108"
user = "root"
passw = "aioria"
host = "34.175.221.108"
database = "main"

# Define the API key
headers = {'x-api-key': 'APP2023'}

# Connect to the database
def connect():
    """
    Creates a database connection using the given parameters and returns the connection object.
    Returns:
        conn: The database connection object.
    """
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def load_data(path):
    """
    Loads data from the given URL path and returns the 'result' key of the JSON response.
    Args: path: The URL path to load the data from.
    Returns: The 'result' key of the JSON response.
    """
    result = requests.get(path, headers=headers).json()
    print(result)
    return result['result']

def delete_data(path):
    """
    Deletes data from the given path
    Args: path: The URL path to delete the data from.
    Returns: Nothing
    """
    requests.delete(path, headers=headers)
    return

def create_data(path, data):
    """
    Creates data from the given path
    Args: path: The URL path to create the data from.
          data: The data to be created
    Returns: Nothing
    """
    requests.post(path, json=data, headers=headers)
    return
    



# Index page
@app.route("/")
# @login_required # This decorator is not needed as I want everybody to view the index page to be able to subscribe
def index():
    """
    Takes you to the index page. Just renders the index page
    """

    return render_template("index.html"), 200

# Create new pet
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
        data = {
            "name" : request.form.get("petname"),
            "lastname" : request.form.get("lastname"),
            "age" : request.form.get("age"),
            "specie" : request.form.get("specie"),
            "pet_id" : session["user_id"] }

        path = f"{ip_api}/pet/create"
        create_data(path, data)
        

        return redirect('/mypets')



# Shows a specific pet. This function also allows the user to add a new history to the pet
@app.route("/<int:pet_num>", methods=["POST", "GET"])
@login_required
def showpet(pet_num):
    """
    Displays the information and history of a pet with the given ID.
    Args: pet_num (int): The ID of the pet to display.
    Returns: A Flask HTTP response containing the rendered HTML template and a status code.
    """
    # If user want's to add a new history to the pet
    if request.method == "POST":
        # Create JSON object to send to the API
        data = {
            "pet_id": session["user_id"],
            "story": request.form.get("history"),
            "pet_num": pet_num
        }
        path = f"{ip_api}/pet/create_history"
        create_data(path, data)
        
    # If user just wants to view the pet's history
    # Create path to get the pet's information & history and load the data from the api
    path = f"{ip_api}/pet/{pet_num}"
    pets = load_data(path)
    path = f"{ip_api}/pet/{pet_num}/history"
    history = load_data(path)        

    return render_template("showpet.html", pets=pets, history=history), 200


@app.route("/deletehist/<int:histnum>", methods=["POST", "GET"])
@login_required
def deletehist(histnum):
    """
    This function allows the user to delete a history from the database.
    User must be logged in in order to delete a history.
    If user not logged in, then redirected to index page
    Args: histnum (int): The ID of the history to delete.
    Return: Redirects to the showpet page with the pet_num of the pet that the history belongs to
    """

    # Load the pet number for the history to delete from the API
    path = f"{ip_api}/pet/gpn/{histnum}"
    pet_num = load_data(path)
    pet_num = pet_num['pet_num']

    # Send a DELETE request to the API to delete the history
    path = f"{ip_api}/pet/delete_history/{histnum}"
    delete_data(path)
    

    return redirect(url_for('showpet', pet_num = pet_num))


@app.route("/deletepet/<int:pet_num>", methods=["POST", "GET"])
@login_required
def deletepet(pet_num):
    """
    Function to delete a pet from the database
    It also deletes all the history associated with the pet
    User must be logged in in order to delete a pet.
    """

    # Send a DELETE request to the API to delete the pet
    path = f"{ip_api}/pet/delete/{pet_num}"
    delete_data(path)

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

        username = request.form.get("username")
        path = f"{ip_api}/user/{username}"
        rows = load_data(path)

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
    """
    Log user out
    User gets redirected to the index page
    """

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register user
    Once the user has registered, they are redirected to the log in page
    They must log in in order to access the rest of the website
    """

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
        
        # Get new username
        usr = request.form.get("username")
        
        # Get from db users with that username
        path = f"{ip_api}/user/{usr}"
        rows = load_data(path)

        # Check if user already exists
        if len(rows) == 1:
            return apology("Username already in use", 400)
        
        # If it does not exist, then insert it
        pwd = generate_password_hash(request.form.get("password"))
        data = {"username": usr, "hash": pwd}
        path = f"{ip_api}/user/new"
        create_data(path, data)

        # Redirect user to home page
        return redirect("/login")


@app.route("/mypets", methods=["GET", "POST"])
@login_required
def mypets():
    """
    Function to show the pets of the user
    User must be logged in in order to see their pets
    """

    # Load the user's pets and history data from the API
    id = session["user_id"]
    path = f"{ip_api}/pet/gp/{id}"
    pets = load_data(path)
    path = f"{ip_api}/pet/gh/{id}"
    history = load_data(path)

    return render_template("mypets.html", pets=pets, history=history)


def errorhandler(e):
    """
    Handle HTTP errors.
    Args: e: The error object to handle.
    Returns: HTTP response containing an apology message and the HTTP error code.
    """
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# Use to run local or App Engine
if __name__ == '__main__':
    app.run(debug=True, port=8080)