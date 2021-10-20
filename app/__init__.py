# Importación del framework usado, Flask
from flask import Flask

from .config import Config
from .models import db

# Definición de la creación de la app
def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    return app