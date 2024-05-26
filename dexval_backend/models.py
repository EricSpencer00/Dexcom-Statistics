# Interact with the database
# Path: dexval_backend/models.py

'''
Make a call to a database called DexVal.db
The DB is hosted on localhost
MDGL_Numbers, int
time, datetime, iterated every 5 minutes
id, int, primary key
notification, boolean, default False

Will need to update, delete, and insert MDGL_numbers
Will need to update, delete, and insert notifications
Will need to update time every 5 minutes and therefore update MDGL_numbers
id = mdgl_numbers = time = notification
when updating one value, update all values, refer to id of point
'''

from dexval_backend.config import db
import datetime
import json

class MDGLNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mdgl_numbers = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    notification = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"MDGLNumbers('{self.mdgl_numbers}', '{self.time}', '{self.notification}')"

    def update_all(self, mdgl_numbers, notification):
        self.mdgl_numbers = mdgl_numbers
        self.notification = notification
        self.time = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def insert(mdgl_numbers, notification=False):
        new_entry = MDGLNumbers(
            mdgl_numbers=mdgl_numbers,
            time=datetime.datetime.utcnow(),
            notification=notification
        )
        db.session.add(new_entry)
        db.session.commit()

    @staticmethod
    def delete_by_id(entry_id):
        entry = MDGLNumbers.query.get(entry_id)
        if entry:
            db.session.delete(entry)
            db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'mdglNumbers': self.mdgl_numbers,
            'time': self.time.isoformat(),
            'notification': self.notification
        }

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Notifications('{self.notification}', '{self.time}')"

    def to_json(self):
        return {
            'id': self.id,
            'notification': self.notification,
            'time': self.time.isoformat()
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    glucose_readings = db.relationship('MDGLNumbers', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.first_name}', '{self.last_name}')"

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'createdAt': self.created_at.isoformat()
        }
