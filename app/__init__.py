from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()  # Load from .env

    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///database.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # OAuth Setup
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
