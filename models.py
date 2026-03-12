"""
Database Models Module

Defines the SQLAlchemy ORM models for the application's SQLite database.
Contains two models:
- Data: Stores temperature readings with timestamps.
- User: Stores registered user accounts with hashed passwords.
"""

from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Data(db.Model):
    """
    Represents a single temperature measurement record.

    Attributes:
        id (int): Auto-incrementing primary key.
        timestamp (str): The date and time of the measurement (format: 'DD.MM.YYYY HH:MM').
        temp (float): The recorded temperature value in degrees Celsius.
    """
    id=db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(32), nullable=False)
    temp = db.Column(db.Float, nullable=False)

    def __init__(self,timestamp,temp):
        self.temp=temp
        self.timestamp=timestamp


class User(db.Model):
    """
    Represents a registered user account.

    Attributes:
        id (int): Auto-incrementing primary key.
        username (str): Unique username (minimum 4 characters).
        password (str): SHA-256 hashed password.
        email (str): Unique email address.
    """
    __tablename__="users"


    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(120), nullable=False)
    email=db.Column(db.String(120), nullable=False)


    def __init__(self,username,password,email):
        self.username=username
        self.password=password
        self.email=email
