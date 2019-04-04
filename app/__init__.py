from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)
    app.config.from_object('config.Config')

    with app.app_context():
        from . import routes
        
        # db.drop_all()
        db.create_all()

        return app