# Importación del framework usado, Flask
from flask import Flask

# Importancion de las configuraciones y blueprints
from .config import Config
from .models import db, ma
from .auth import auth
from .panel import panel
from .auth.views import login_manager

# Definición de la creación de la app
def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(auth)
    app.register_blueprint(panel)

    login_manager.init_app(app)


    db.init_app(app)
    ma.init_app(app)
    return app