# create / POST
# - first_name
# - last_name
# - email
# - password
# - time
# - notification
# - id
# - mdgl_numbers

# read / GET
# - first_name
# - last_name
# - email
# - password
# - time
# - notification
# - id
# - mdgl_numbers

# update / PUT
# - first_name
# - last_name
# - email
# - password
# - time
# - notification
# - id
# - mdgl_numbers

# delete / DELETE
# - id
# - mdgl_numbers
# - time
# - notification

from flask import Flask, request, jsonify
from config import app, db
from models import MDGLNumbers, Notifications, User
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

CORS(app)

import os
from dotenv import load_dotenv
load_dotenv()

'''____________TIME____________'''

@app.route('/api/time', methods=['GET'])
def get_time():
    return jsonify({'time': datetime.datetime.utcnow().isoformat()})

@app.route('/api/time', methods=['POST'])
def create_time():
    data = request.get_json()
    return jsonify({'time': data['time']})

@app.route('/api/time/<int:id>', methods=['PUT'])
def update_time(id):
    data = request.get_json()
    return jsonify({'time': data['time']})

@app.route('/api/time/<int:id>', methods=['DELETE'])
def delete_time(id):
    return jsonify({'message': 'Deleted'})

'''____________USER____________'''

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    db.session.commit()
    return jsonify(user.to_json())

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):    
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

'''____________MDGL____________'''

@app.route('/api/mdgl_numbers', methods=['GET'])
def get_mdgl_numbers():
    mdgl_numbers = MDGLNumbers.query.all()
    return jsonify([mdgl_number.to_json() for mdgl_number in mdgl_numbers])

@app.route('/api/mdgl_numbers', methods=['POST'])
def create_mdgl_number():
    data = request.get_json()
    mdgl_number = MDGLNumbers(mdgl_numbers=data['mdgl_numbers'], notification=data.get('notification', False))
    db.session.add(mdgl_number)
    db.session.commit()
    return jsonify(mdgl_number.to_json())

@app.route('/api/mdgl_numbers/<int:id>', methods=['PUT'])
def update_mdgl_number(id):
    mdgl_number = MDGLNumbers.query.get(id)
    if not mdgl_number:
        return jsonify({'error': 'MDGL number not found'}), 404
    data = request.get_json()
    mdgl_number.mdgl_numbers = data.get('mdgl_numbers', mdgl_number.mdgl_numbers)
    mdgl_number.notification = data.get('notification', mdgl_number.notification)
    mdgl_number.time = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(mdgl_number.to_json())

@app.route('/api/mdgl_numbers/<int:id>', methods=['DELETE'])
def delete_mdgl_number(id):
    mdgl_number = MDGLNumbers.query.get(id)
    if not mdgl_number:
        return jsonify({'error': 'MDGL number not found'}), 404
    db.session.delete(mdgl_number)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

'''____________NOTIFICATIONS____________'''

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    notifications = Notifications.query.all()
    return jsonify([notification.to_json() for notification in notifications])

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    notification = Notifications(notification=data['notification'])
    db.session.add(notification)
    db.session.commit()
    return jsonify(notification.to_json())

@app.route('/api/notifications/<int:id>', methods=['PUT'])
def update_notification(id):
    notification = Notifications.query.get(id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    data = request.get_json()
    notification.notification = data.get('notification', notification.notification)
    notification.time = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(notification.to_json())

@app.route('/api/notifications/<int:id>', methods=['DELETE'])
def delete_notification(id):
    notification = Notifications.query.get(id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5005)
