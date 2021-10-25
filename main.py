from flask import render_template
from app import create_app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os

# Crear base de datos si esta no existe
engine = create_engine("mariadb+mariadbconnector://root:root@mysqldb/SenaSoft")
if not database_exists(engine.url):
    create_database(engine.url)
    os.system('python dbCreator.py')
else:
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
    try:
        os.system('python dbCreator.py')
    except:
        print("error creating db")
        
    app.run(host='0.0.0.0', port=5000, debug=True)
