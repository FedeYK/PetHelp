# <a name='PetHelp!'></a>PetHelp!

### General Description:

This project was developed to help vet's keep their medical history from their patients. In this web app, vet's will be able to create new pets with all the information they need and then submit information about that pet every time they need it.

## <a name='Table of Contents'></a>Table of Contents

* [Instructions](#Instructions)
* [How to run](#HowToRun)
* [How to use](#HowToUse)
* [Functions](#Functions)
  * what


I used a database with three tables. Each table saves specific information of each user.

The tables are:
users:

    Here the username, hash and user_id are saved.
    With the user ID I am able to join all the tables and to get the exact information you need.

pets:

    Pets saves the name, lastname, age and specie of each pet. Also, its linked with each user by the pet_id number, which is created by the newpet function getting the user id from the user that has log on.
    Each pet, has a pet_num to be able to identify each pet. This is a primary key and links each pet with each user.

history:

    In history table, each pet medical hisotry is stored.
    History saves the date the new entry is entered, the history itselve the pet number and pet id to be able to link it to each pet and each user and a number which states the history number.
    The history number is then used in case you need to delete a history. By using a history number you can't delete a history you didn't wanted.

They can also delete pets and history of each pet.

### application.py

This is the heart of the app. Here, all the functions are developed in order to create a new user, a new pet, add a new history for the pet and delete information.

The functions developed are:
index -> returns index.htm
newpet -> When method = GET, it redirects to newpet.html script. If method is POST, the function requests all the information inserted in the form and then inserts a new line in the database with that information.




showpet -> Shows a specific pet that you asked for. You can also add a history when method is POST and then it refreshes the same showpet.html
deletehist -> Used to delete some history added to a pet. Then it redirects you to showpet function
login -> Used to log in with your user.
logout -> Logs out your user
register -> Used to register a new user
mypets -> shows all your pets, need to be loged in

### layout.html

Base HTML script, the main feature is a navegation bar where you can login or register in case you are not logged in and you can view your pets or add a new pet or log out if you are logged in.

### index.html

In the index there is a small description of the web app, where vets can learn what this app is for.

### login.html

HTML script where you can log in to your account

### register.html

HTML script where you can register a new user. Consists of a form with trhee imputs for username, password and confirm password.

### mypets.html

HTML script where using a for loop all your pets will be shown in a table showing you their name, lastname, age and specie. You can enter an view the pet history or delete the pet.

### newpet.html

HTML script where you can create a new pet. Using a form and several imputs you can create a new pet

### showpet.html

HTML script that shows the information of each pet you select. Here, using a for loop you can see all the information of the pet and also the history. You can add new history or delete previous history from it.



