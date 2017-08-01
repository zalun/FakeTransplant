from flask import Flask
from transplant.views import app_blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(app_blueprint)

    return app
