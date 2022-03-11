from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Hike:
    database = "hikes"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.location = data["location"]
        self.date = data["date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    # =====CLASS METHODS=====

    # Create hike
    @classmethod
    def save(cls, data):
        query = "INSERT INTO hikes (title, description, location, date, created_at, updated_at, user_id) VALUES (%(title)s, %(description)s, %(location)s, %(date)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.database).query_db(query, data)

    # Update hike
    @classmethod
    def update(cls, data):
        query = "UPDATE hikes SET title = %(title)s, description = %(description)s, location = %(location)s, date = %(date)s WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query, data)

    # Get all hikes
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM hikes;"
        results = connectToMySQL(cls.database).query_db(query)
        return results
    
    # Get one hike by id
    @classmethod
    def get_one(cls, data):
        query = "SELECT * from hikes WHERE id = %(id)s;"
        return cls(connectToMySQL(cls.database).query_db(query, data)[0])

    # Delete hike
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM hikes WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query, data)

    # =====STATIC METHODS=====

    # Validate new hike
    @staticmethod
    def validate_hike(hike):
        is_valid = True
        if len(hike["title"]) == 0:
            flash("Title is required")
            is_valid = False
        if len(hike["title"]) < 5:
            flash("Title must be at least 5 characters")
            is_valid = False
        if len(hike["description"]) == 0:
            flash("Description is required")
            is_valid = False
        if len(hike["description"]) < 7:
            flash("Description must be at least 7 characters")
            is_valid = False
        if len(hike["location"]) == 0:
            flash("Location is required")
            is_valid = False
        if len(hike["location"]) < 3:
            flash("Location must be at least 3 characters")
            is_valid = False
        return is_valid