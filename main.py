from flask import render_template
from app import create_app

app = create_app()

# Creacion de ruta principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/404')
def error():
    return render_template('404.html')

