from flask import request, jsonify
from app import app, db
from models import User, Role
from flask_jwt_extended import create_access_token, jwt_required

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # In a real app, hash this
    role = data.get('role', 'User')  # Default role is 'User'
    
    user_role = Role.query.filter_by(name=role).first() or Role(name=role)
    db.session.add(user_role)
    db.session.commit()

    new_user = User(username=username, password=password, role=user_role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # In a real app, compare hashed passwords

    user = User.query.filter_by(username=username, password=password).first()

    if not user:
        return jsonify({"message": "Invalid credentials!"}), 401

    access_token = create_access_token(identity={'username': user.username})
    return jsonify(access_token=access_token)
