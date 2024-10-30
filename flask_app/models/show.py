from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL

# from flask_app.models import show
import re
from pprint import pprint
from flask_app.models.user import User
from flask import flash


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class Show:
    """This Show class."""

    _db = "nextfix_db"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data["release_date"]
        self.comment = data["comment"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        """This method validates the Show registration form"""
        is_valid = True

        if len(form_data["title"].strip()) == 0:
            flash("Please enter Show name.")
            is_valid = False
        elif len(form_data["title"].strip()) < 3:
            flash("Show name must be at least three characters.")
            is_valid = False
        if len(form_data["network"].strip()) == 0:
            flash("Please enter Network.")
            is_valid = False
        elif len(form_data["network"].strip()) < 3:
            flash("Network must be at least three characters.")
            is_valid = False
        if len(form_data["release_date"].strip()) == 0:
            flash("Please enter release date.")
            is_valid = False
        if len(form_data["comment"].strip()) == 0:
            flash("Please enter Comments.")
            is_valid = False
        elif len(form_data["comment"].strip()) < 3:
            flash("Comments must be at least three characters.")
            is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):
        """This method finds all the shows in the database."""

        query = "SELECT * FROM shows:"
        list_of_dicts = connectToMySQL(Show._db).query_db(query)
        pprint(list_of_dicts)
        shows = []

        for each_dict in list_of_dicts:
            show = Show(each_dict)
            shows.append(show)

        return shows

    @classmethod
    def find_all_with_users(cls):
        """This method finds all the shows with users in the database."""

        query = """
        SELECT * FROM shows
        JOIN users
        ON shows.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Show._db).query_db(query)
        shows = []

        for each_dict in list_of_dicts:
            show = Show(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            result = User(user_data)
            show.user = result
            shows.append(show)

        return shows

    @classmethod
    def create(cls, form_data):
        """This method creates a show from a form."""

        query = """
        INSERT INTO shows
        (title, network, release_date, comment, user_id)
        VALUES
        (%(title)s, %(network)s, %(release_date)s, %(comment)s, %(user_id)s);
        """
        shows_id = connectToMySQL(Show._db).query_db(query, form_data)

        return shows_id


    @classmethod
    def find_by_email(cls, email):
        """This method finds a show by email."""

        query = """SELECT * FROM shows WHERE email = %(email)s;"""
        data = {"email": email}
        list_of_dicts = connectToMySQL(Show._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        show = Show(list_of_dicts[0])
        return show

    @classmethod
    def find_by_show_id(cls, show_id):
        """This method finds a show by show_id."""

        query = """SELECT * FROM shows WHERE id = %(show_id)s;"""
        data = {"show_id": show_id}
        list_of_dicts = connectToMySQL(Show._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        show = Show(list_of_dicts[0])
        return show

    @classmethod
    def find_by_user_id(cls, show_id):
        """This method finds a show and the user by the show id."""
        query = """
        SELECT * FROM shows
        JOIN users
        ON shows.user_id = users.id
        WHERE shows.id = %(show_id)s;
        """
        data = {"show_id": show_id}
        list_of_dicts = connectToMySQL(Show._db).query_db(query, data)
        pprint(list_of_dicts)
        show = Show(list_of_dicts[0])
        one_dict = list_of_dicts[0]
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }

        user = User(user_data)
        show.user = user
        return show

    @classmethod
    def update(cls, form_data):
        """This method updates a show in the database."""
        print("\n\n\n\n\line247: ", form_data)
        query = """
        UPDATE shows
        SET title = %(title)s,
        network = %(network)s,
        release_date = %(release_date)s
        WHERE id = %(show_id)s;
        """

        connectToMySQL(Show._db).query_db(query, form_data)
        return

    @classmethod
    def delete(cls, show_id):
        """This method deletes a show in the database"""

        query = """
        DELETE FROM shows
        WHERE id = %(show_id)s;
        """
        data = {"show_id": show_id}
        return connectToMySQL(Show._db).query_db(query, data)
