from flask import request, jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from app.models import User
from app import db
from app.swagger import api, user_model, login_model

@api.route('/register')
class RegisterUser(Resource):
    @api.expect(user_model)
    @api.response(201, 'User successfully registered.')
    @api.response(400, 'Bad Request')
    def post(self):
        """Register a new user"""
        data = request.json
        
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
            is_admin=data['is_admin']
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User registered successfully'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'User with this email already exists'}, 400

@api.route('/login')
class LoginUser(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful.')
    @api.response(401, 'Invalid credentials.')
    def post(self):
        """Authenticate a user and return a JWT token"""
        data = request.json

        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password_hash, data['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200

@api.route('/admin_only_page')
class AdminOnlyPage(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    @api.response(200, 'Admin access granted.')
    @api.response(403, 'Admin access only.')
    def get(self):
        """Accessible only to admin users"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.is_admin:
            return {'message': f'Hello {user.first_name}'}, 200
        else:
            return {'error': 'Admin access only'}, 403

@api.route('/all_users')
class AllUsersPage(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    @api.response(200, 'User access granted.')
    def get(self):
        """Accessible to all authenticated users"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return {'message': f'Hello {user.first_name}'}, 200

@api.route('/visitor')
class VisitorPage(Resource):
    @api.response(200, 'Visitor access granted.')
    def get(self):
        """Accessible to anyone including unauthenticated visitors"""
        return {'message': 'Hello Visitor'}, 200
