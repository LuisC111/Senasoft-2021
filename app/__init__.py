# Importación del framework usado, Flask
from flask import Flask

from .config import Config
from .models import db
from .auth import auth

# Definición de la creación de la app
def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(auth)

    db.init_app(app)
    return app