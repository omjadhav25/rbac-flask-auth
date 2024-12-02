from flask import request, jsonify
from app import app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Role

@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    
    if user.role.name == 'Admin':
        return jsonify({"message": "Welcome, Admin!"})
    elif user.role.name == 'User':
        return jsonify({"message": "Welcome, User!"})
    else:
        return jsonify({"message": "Access Denied!"}), 403
