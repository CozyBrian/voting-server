import os

from flask import Flask 

from extensions import db
from routes import main
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    
    db.init_app(app)

    app.register_blueprint(main)

    return app

if "name" == "app":
    create_app()