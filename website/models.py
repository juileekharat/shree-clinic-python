from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    blood_group = db.Column(db.String(150))
    treatment = db.Column(db.String(300))
    patient_since = db.Column(db.Date())
    history = db.Column(db.String(300))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())

@dataclass
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer ,db.ForeignKey('user.id'))

@dataclass
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
    

