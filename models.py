from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Data(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(32), nullable=False)
    temp = db.Column(db.Float, nullable=False)

    def __init__(self,timestamp,temp):
        self.temp=temp
        self.timestamp=timestamp


class User(db.Model):
    __tablename__="users"


    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(120), nullable=False)
    email=db.Column(db.String(120), nullable=False)


    def __init__(self,username,password,email):
        self.username=username
        self.password=password
        self.email=email
