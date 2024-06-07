# backend/app/resources/auth/admin_api.py
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.model import db, User, bcrypt

def register_store_manager():
        
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'message': 'Store Manager already exists.'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_store_manager = User(username=data['username'], email=data['email'], password=hashed_password, role='store-manager', is_approved=0)
    db.session.add(new_store_manager)
    db.session.commit()
    return jsonify({'message': 'Successfully captures the request for Store Manager Role.\nPlease wait for the approval by Admin.'}), 201

def approve_store_manager(user_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        store_manager = User.query.get(user_id)
        if store_manager and store_manager.role == 'store-manager' and not store_manager.is_approved:
            store_manager.is_approved = True
            db.session.commit()
            return jsonify({'message': 'Store Manager approved successfully.'}), 200
        else:
            return jsonify({'message': 'Invalid request.'}), 400
    else:
        return jsonify({'message': 'Permission denied. Only admins can approve store managers.'}), 403 