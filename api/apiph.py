from sqlalchemy import create_engine, text
from flask_restx import Api, Namespace, Resource, reqparse, inputs, fields
from flask import Flask, jsonify, request
from sqlalchemy.engine.row import RowMapping

# Configure application
app = Flask(__name__)

# Defining API key for authentication
api_key = "APP2023"

# Define decorator for checking API key
def require_api_key(func):
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('X-API-KEY')
        if provided_key == api_key:
            return func(*args, **kwargs)
        else:
            return {'message': 'Invalid API key'}, 401
    return wrapper

# Define the API & version & description
api = Api(app, version = '1.0',
    title = 'Rest Api to feed Streamlit App',
    description = """
        Rest Api to feed PetHelp App
        The database is hosted on a Google Cloud Platform Cloud SQL instance.
        """,
    contact = "frbarca@student.ie.edu",
    endpoint = "/api/ph/v1"
)


# Database Data
user = "root"
passw = ""
host = ""
database = "main"

# Connect to the database
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

# If you want to use a file database, uncomment the following lines
# In this case, we are connecting to a file database called mypets.db

# engine = create_engine("sqlite:///mypets.db")
# def connect():
#     return engine.connect()


# Create a namespace for pets
pets = Namespace('pets',
    description = 'All operations related to pets',
    path='/api/ph/v1')
api.add_namespace(pets)

# Create a namespace for users
users = Namespace('users',
    description = 'All operations related to users',
    path='/api/ph/v1')
api.add_namespace(users)


@pets.route('/pet/<int:pet_num>')
class Pet(Resource):
    @require_api_key
    def get(self, pet_num):
        # Connect to the database and execute a SQL query to retrieve the pet data
        with connect() as db:
            result = db.execute(text(f"SELECT * FROM pets WHERE pet_num = '{pet_num}'")).fetchall()
        return jsonify({'result': [dict(row) for row in result]})
   
@pets.route('/pet/<int:pet_num>/history')
class PetHist(Resource):
    @require_api_key
    def get(self, pet_num):
        # Connect to the database and execute a SQL query to retrieve the pet data
        with connect() as db:
            result = db.execute(text(f"SELECT * FROM history WHERE pet_num = '{pet_num}'")).fetchall()
        return jsonify({'result': [dict(row) for row in result]})

@pets.route('/pet/create_history')
class PetHist(Resource):
    @require_api_key
    def post(self):
        # Get a json with pet_id, story, pet_num
        data = request.get_json()
        pet_id = data['pet_id']
        story = data['story']
        pet_num = data['pet_num']
        # Connect to the database and execute a SQL query to retrieve the pet data
        with connect() as db:
            db.execute(text(f"INSERT INTO history (pet_id, story, pet_num) VALUES ('{pet_id}', '{story}', '{pet_num}');"))
        # I dont want to return anything, just the code 201 to vereifies that it was created
        return 201

@pets.route('/pet/create')
class Pet(Resource):
    @require_api_key
    def post(self):
        # Get a json with pet_id, story, pet_num
        data = request.get_json()
        name = data['name']
        lastname = data['lastname']
        age = data['age']
        specie = data['specie']
        id = data['pet_id']
        # Connect to the database and execute a SQL query to retrieve the pet data
        with connect() as db:
            db.execute(text(f"INSERT INTO pets (name, lastname, age, specie, pet_id) VALUES ( '{name}', '{lastname}', '{age}', '{specie}', '{id}')"))
        # I dont want to return anything, just the code 201 to vereifies that it was created
        return 201
    
@pets.route('/pet/delete_history/<int:histnum>')
class DelPetHist(Resource):
    @require_api_key
    def delete(self, histnum):
        # Connect to the database and execute a SQL query to delete the pet history
        with connect() as db:
            db.execute(text(f"DELETE FROM history WHERE histnum = '{histnum}'"))
        return

@pets.route('/pet/delete/<int:pet_num>')
class DelPet(Resource):
    @require_api_key
    def delete(self, pet_num):
        # Connect to the database and execute a SQL query to delete the pet & history
        with connect() as db:
            db.execute(text(f"DELETE FROM pets WHERE pet_num = '{pet_num}'"))
            db.execute(text(f"DELETE FROM history WHERE pet_num = '{pet_num}'"))
        return

@pets.route('/pet/gpn/<int:histnum>')
class GetPetNum(Resource):
    @require_api_key
    def get(self, histnum):
        with connect() as db:
            result = db.execute(text(f"SELECT pet_num FROM history WHERE histnum = '{histnum}'")).fetchone()
        return jsonify({'result': dict(result)})
    
@pets.route('/pet/gp/<int:id>')
class GetPet(Resource):
    @require_api_key
    def get(self, id):
        with connect() as db:
            result = db.execute(text(f"SELECT * FROM pets WHERE pet_id ='{id}'")).fetchall()
        return jsonify({'result': [dict(row) for row in result]})

@pets.route('/pet/gh/<int:id>')
class GetHist(Resource):
    @require_api_key
    def get(self, id):
        with connect() as db:
            result = db.execute(text(f"SELECT * FROM history WHERE pet_id = '{id}'")).fetchall()
        return jsonify({'result': [dict(row) for row in result]})

@users.route('/user/<string:username>')
class GetUserData(Resource):
    @require_api_key
    def get(self, username):
        with connect() as db:
            result = db.execute(text(f"SELECT * FROM users WHERE username = '{username}'")).fetchall()
        return jsonify({'result': [dict(row) for row in result]})

@users.route('/user/new')
class CreateNewUser(Resource):
    @require_api_key
    def post(self):
        data = request.get_json()
        username = data['username']
        hash = data['hash']
        print(username, hash)
        with connect() as db:
            db.execute(text(f"INSERT INTO users (username, hash) VALUES ('{username}', '{hash}')"))
        # return 201



if __name__ == '__main__':
    app.run(debug=True)