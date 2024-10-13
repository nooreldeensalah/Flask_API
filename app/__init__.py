import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade
from dotenv import load_dotenv
from app.swagger import create_api

load_dotenv()

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Customize application configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Initialize extensions with app instance
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Initialize Swagger API
    api = create_api(app)

    # Register Namespaces (from flask-restx)
    from app.routes import api as users_api
    api.add_namespace(users_api, path='/api/users')

    # Apply database migrations automatically
    with app.app_context():
        apply_migrations()

    return app

def apply_migrations():
    """
    Function to apply migrations automatically and create tables if not already existing.
    """
    # Make sure all migrations are applied
    try:
        upgrade()
        print("Migrations applied successfully!")
    except Exception as e:
        print(f"Error applying migrations: {e}")
        db.create_all()
        print("Tables created manually!")
