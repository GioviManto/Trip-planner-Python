from website import user_db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Define the User class, inheriting from user_db.Model and UserMixin
class User(user_db.Model, UserMixin):
    # Define attributes/columns for the User model
    id = user_db.Column(user_db.Integer, primary_key=True)  # Primary key for the User table
    email = user_db.Column(user_db.String(150), unique=True)  # User's email address (unique constraint)
    password = user_db.Column(user_db.String(150))  # Hashed password
    first_name = user_db.Column(user_db.String(150))  # User's first name