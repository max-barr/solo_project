from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import hike

import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    database = "hikes"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.hikes = []

    # =====CLASS METHODS=====

    # Create a new user
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.database).query_db(query, data)

    # Get all users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.database).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    # Get one user by id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return cls(results[0])

    #Get one user by email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Get user with their hikes
    @classmethod
    def get_user_with_hikes(cls, data):
        query = "SELECT * FROM users LEFT JOIN hikes ON users.id = hikes.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        user = cls(results[0])
        print(results)
        # if results[0]["name"] != None:
        for row_from_db in results:
            hike_data = {
                "id" : row_from_db["hikes.id"],
                "title" : row_from_db["title"],
                "description" : row_from_db["description"],
                "location" : row_from_db["location"],
                "date" : row_from_db["date"],
                "created_at" : row_from_db["hikes.created_at"],
                "updated_at" : row_from_db["hikes.updated_at"]
            }
            user.hikes.append( hike.Hike( hike_data ) )
        return user

    # =====STATIC METHODS=====

    # Validate registration
    @staticmethod
    def validate_registration(data):
        is_valid = True
        #First name cannot be blank
        if len(data["first_name"]) == 0:
            is_valid = False
            flash("First name is required", "error")
        #Last name cannot be blank
        if len(data["last_name"]) == 0:
            is_valid = False
            flash("Last name is required", "error")
        #Email can't be blank
        if len(data["email"]) == 0:
            is_valid = False
            flash("Email address is required", "error")
        #First name min 2 characters
        if len(data["first_name"]) < 2:
            is_valid = False
            flash("First name must be at least 2 characters", "error")
        #Last name min 2 characters
        if len(data["last_name"]) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters", "error")
        #Password must be at least 7 characters
        if len(data["password"]) < 7:
            is_valid = False
            flash("Password must be at least 7 characters", "error")
        #Email must be an email address
        if not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("We're sorry, that email address is invalid", "error")
        #Passwords match
        if data["password"] != data["confirm_password"]:
            is_valid = False
            flash("We're sorry, your passwords don't match", "error")
        #Email must be unique
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.database).query_db(query, data)
        #results returns list of dictionaries
        if len(results) >= 1:
            is_valid = False
            flash("We're sorry, that email is already taken", "error")
        return is_valid

    # Validate login
    @staticmethod
    def validate_login(data):
        is_valid = True
        if len(data["email"]) == 0:
            is_valid = False
            flash("Email address is required", "error")
        if len(data["password"]) == 0:
            is_valid = False
            flash("Password is required", "error")
        return is_valid
