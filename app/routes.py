from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all([data.get('first_name'), data.get('last_name'), data.get('email'),
                data.get('phone_number'), data.get('password')]) or data.get('is_admin') is None:
        return jsonify({'error': 'All fields are required'}), 400

    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        password_hash=hashed_password,
        is_admin = data['is_admin']
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        return jsonify({'error': 'User with this email already exists'}), 400

@main_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

