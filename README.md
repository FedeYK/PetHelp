# <a name='PetHelp!'></a>PetHelp!

### General Description:

This project is a Flask web application was developed to help vet's keep their medical history from their patients. In this web app, vet's will be able to create new pets with all the information they need and then submit information about that pet every time they need it. PetHelp App allows users to manage information about their pets, including a history of events or incidents. Users can create, update, and delete pets, and add, view or delete histories for each pet.

## <a name='Table of Contents'></a>Table of Contents


* [Instructions & general description](#instructions)
* [HTML Descriptions](#html)
* [How to setup & run](#howtorun)
* [How to use](#howtouse)
* [Routes & API Endpoints](#routes)
* [Database Description](#dbdesc)


### <a name='instructions'></a> PetHelp Instrucitons and general description

This is the heart of the app. Here, all the functions are developed in order to create a new user, a new pet, add a new history for the pet and delete information.

The functions developed are:
index -> returns index.html
newpet -> When method = GET, it redirects to newpet.html script. If method is POST, the function requests all the information inserted in the form and then inserts a new line in the database with the use of an API with that information.

showpet -> Shows a specific pet that you asked for. You can also add a history when method is POST and then it refreshes the same showpet.html
deletehist -> Used to delete some history added to a pet. Then it redirects you to showpet function
login -> Used to log in with your user.
logout -> Logs out your user
register -> Used to register a new user
mypets -> shows all your pets, need to be loged in

### <a name='html'></a> HTML Description

#### layout.html

Base HTML script, the main feature is a navegation bar where you can login or register in case you are not logged in and you can view your pets or add a new pet or log out if you are logged in.

#### index.html

In the index there is a small description of the web app, where vets can learn what this app is for.

#### login.html

HTML script where you can log in to your account

#### register.html

HTML script where you can register a new user. Consists of a form with trhee imputs for username, password and confirm password.

#### mypets.html

HTML script where using a for loop all your pets will be shown in a table showing you their name, lastname, age and specie. You can enter an view the pet history or delete the pet.

#### newpet.html

HTML script where you can create a new pet. Using a form and several imputs you can create a new pet

#### showpet.html

HTML script that shows the information of each pet you select. Here, using a for loop you can see all the information of the pet and also the history. You can add new history or delete previous history from it.

### <a name='howtorun'></a>How to setup and run

1. Clone the repository or download the code.
2. Install the required packages: **`pip install -r requirements.txt`**
3. Configure your MySQL database connection parameters in the **`connect()`** function of api.py.
4. Run the API
5. Run the application

### <a name='howtouse'></a>How to use

Once you are able to run the application, first you have to create an account.
If you have the account already created just add a pet!
Then you can ask the app to show you all your pets.
When you ask the web app to show you a specific pet, it will show you that pet and their specific stories... if it doesn't have any, just add them and start using it!
Have fun!

### <a name='routes'></a>Routes & API Endpoints

#### Routes

- **`/`**: Index page.
- **`/newpet`**: Add a new pet.
- **`/login`**: User login.
- **`/logout`**: User logout.
- **`/register`**: User registration.
- **`/mypets`**: List of user's pets.
- **`/<int:pet_num>`**: View a specific pet and its history.
- **`/deletehist/<int:histnum>`**: Delete a pet's history.
- **`/deletepet/<int:pet_num>`**: Delete a pet.

#### API Endpoints - USER

- **`/api/ph/v1/user/<username>`**: Get user information by username.
- **`/api/ph/v1/user/new`**: Create a new user.

#### API Endpoints - PET

- **`/api/ph/v1/pet/create`**: Create a new pet.
- **`/api/ph/v1/pet/<pet_num>`**: Get pet information by pet ID.
- **`/api/ph/v1/pet/<pet_num>/history`**: Get pet history by pet ID.
- **`/api/ph/v1/pet/create_history`**: Create a new pet history.
- **`/api/ph/v1/pet/gpn/<histnum>`**: Get pet number from a history ID.
- **`/api/ph/v1/pet/delete_history/<histnum>`**: Delete a pet history by history ID.
- **`/api/ph/v1/pet/delete/<pet_num>`**: Delete a pet by pet ID.

### <a name='dbdesc'></a>Database Description

For this project three databases were used. 

The tables are:
#### users:

    This table is used to save the users information, username and password

    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY
    username TEXT,
    hash TEXT

#### pets:

    Pets saves the name, lastname, age and specie of each pet. Also, its linked with each user by the pet_id number, which is created by the newpet function getting the user id from the user that has log on.
    Each pet, has a pet_num to be able to identify each pet. This is a primary key and links each pet with each user.

    pet_num INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name TEXT,
    lastname TEXT,
    age INTEGER,
    specie TEXT,
    pet_id INTEGER
    
    
#### history:

    In history table, each pet medical hisotry is stored.
    History saves the date the new entry is entered, the history itselve the pet number and pet id to be able to link it to each pet and each user and a number which states the history number.
    The history number is then used in case you need to delete a history. By using a history number you can't delete a history you didn't wanted.
    They can also delete pets and history of each pet.
    
    pet_id INTEGER NOT NULL,
    pet_num INTEGER NOT NULL,
    story TEXT,
    date DATETIME DEFAULT NOW(),
    histnum INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY
