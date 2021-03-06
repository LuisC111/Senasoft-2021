from flask import render_template
from app import create_app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os

# Crear base de datos si esta no existe
engine = create_engine(os.getenv('CONNECTION_STRING', 'mariadb+mariadbconnector://root:''@127.0.0.1:3306/SenaSoft'))
if not database_exists(engine.url):
    create_database(engine.url)
    os.system('python dbCreator.py')

app = create_app()

# Handler de error 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


# Creacion de ruta principal
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    if os.getenv('PRODUCTION'):
        os.system('python dbCreator.py')
    
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=True)