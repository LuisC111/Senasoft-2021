from flask import Blueprint

# Creacion de la ruta general auth, la cual tendra todo los metodos de inicio sesions
panel = Blueprint('panel', __name__, url_prefix='/panel')

from . import views