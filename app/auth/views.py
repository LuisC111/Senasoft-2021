from flask import render_template, request, Response, flash, url_for, redirect
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
from . import auth
from ..models import Usuario, db

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Tienes que iniciar primero sesion"
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id):
    try:
        return Usuario.query.get(user_id)
    except:
        return None

# Creacion de la ruta login, con sus metodos tanto para front como para back
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correoUsuario = request.form['mailUsuario']
        passUsuario = request.form['passUsuario']

        # Busqueda en base de datos si el usuario existe y sus crendenciales coinciden
        usuarioData = Usuario.query.filter(Usuario.correoUsuario == correoUsuario, Usuario.contraseñaUsuario == passUsuario).first()
        
        if usuarioData:
            login_user(usuarioData)
            flash('El usuario se ha logeado correctamente!', 'success')
            return redirect('/perfil')
        else:
            flash('Error en usuario o contraseña', 'error')

    if current_user.is_authenticated:
        flash('Ya te encuentras logeado, si deseas utilizar otra cuenta cierra sesion primero', 'info')
        return redirect(url_for('paginaCliente'))
    else:
        return render_template('login.html')

    return render_template('login.html')

# Creacion de la ruta register, con sus metodos tanto para front como para back
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombreUsuario = request.form['']
        apellidoUsuario = request.form['']
        correoUsuario = request.form['']
        passUsuario = request.form['']

        # Busqueda en base de datos si el usuario existe
        usuarioData = Usuario.query.filter(Usuario.correoUsuario == correoUsuario).first()

        if (usuarioData):
            flash('Este correo ya se encuentra registrado!', 'error')
        else:
            # Creacion de un nuevo usuario en caso de ser nuevo
            newUsuario = Usuario(correoUsuario, passUsuario, nombreUsuario, apellidoUsuario)
            db.session.add(newUsuario)
            db.session.commit()

            flash('El usuario se ha registrado correctamente!', 'success')
            return redirect('/login')

    if current_user.is_authenticated:
        flash('Ya te encuentras logeado, si deseas utilizar otra cuenta cierra sesion primero', 'info')
        return redirect(url_for('paginaCliente'))
    else:
        return render_template('login.html')

    return render_template('register.html')

# Creacion de la ruta register, con sus metodos tanto para front como para back
@auth.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfilUsuario():
    return render_template('perfilUsuario.html')