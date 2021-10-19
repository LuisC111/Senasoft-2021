from app import create_app

app = create_app()

@app.route('/')
def index():
    return "hola"