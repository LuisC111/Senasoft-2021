# Importación del framework usado, Flask
from flask import Flask

# Definición de la creación de la app
def create_app():
    app = Flask(__name__)

    return app