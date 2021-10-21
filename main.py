from flask import render_template
from app import create_app

app = create_app()

# Handler de error 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

# Creacion de ruta principal
@app.route('/')
def index():
    return render_template('index.html')


