from flask import Blueprint

# Creacion de la ruta general auth, la cual tendra todo los metodos de inicio sesions
auth = Blueprint('auth', __name__, url_prefix='/auth')

from . import views