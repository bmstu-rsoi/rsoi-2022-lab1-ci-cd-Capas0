import os

from flask import Flask


class AppConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    return app
