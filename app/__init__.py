import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

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

    # Initialize extensions with app instance
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app

