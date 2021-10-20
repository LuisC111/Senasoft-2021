from flask import render_template, request, Response, flash, url_for, redirect, session
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
from . import auth
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..models import Usuario, db
from ..mailing import s
import uuid

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
        return redirect('/auth/perfil')
    else:
        return render_template('login.html')

    return render_template('login.html')

# Creacion de la ruta register, con sus metodos tanto para front como para back
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombreUsuario = request.form['txtNombre']
        apellidoUsuario = request.form['txtApellido']
        correoUsuario = request.form['txtCorreo']
        passUsuario = request.form['txtPassword']
        confirmationHash = str(uuid.uuid4().hex)

        # Busqueda en base de datos si el usuario existe
        usuarioData = Usuario.query.filter(Usuario.correoUsuario == correoUsuario).first()

        if (usuarioData):
            flash('Este correo ya se encuentra registrado!', 'error')
        else:
            # Creacion de un nuevo usuario en caso de ser nuevo
            newUsuario = Usuario(correoUsuario, passUsuario, nombreUsuario, apellidoUsuario, None, None, 0, None, 3, confirmationHash)
            db.session.add(newUsuario)
            db.session.commit()
            
            msg = MIMEMultipart('alternative')

            contextMail = {
                'nombreUsuario' : nombreUsuario,
                'hash' : confirmationHash
            }

            file = render_template('mailAccountConfirmation.html', **contextMail )

            text = """\
            Confirmation mail
            If you dont see the button below
            Just press on the next link:
            localhost:5000/auth/confirm/{}
            """.format(confirmationHash)

            msg['From']= 'david@mi.com.co'
            msg['To']= str(correoUsuario)
            msg['Subject']= "Confirm your email FLOWY"

            part1 = MIMEText(text, "plain")
            part2 = MIMEText(file, "html")

            msg.attach(part1)
            msg.attach(part2)

            s.send_message(msg)

            flash('El usuario se ha registrado correctamente!', 'success')
            return redirect('/auth/login')

    if current_user.is_authenticated:
        flash('Ya te encuentras logueado, si deseas utilizar otra cuenta cierra sesion primero', 'info')
        return redirect(url_for('panel.panelInicio'))
    else:
        return render_template('register.html')

    return render_template('register.html')

# Confirmar email
@auth.route('/confirm/<hash>', methods=['GET', 'POST'])
def confirmMail(hash):
    uniqueHash = hash
    hashExist = Usuario.query.filter(Usuario.confirmationHash == hash).first()
    if hashExist:
        if hashExist.estadoUsuario == 1:
            hashExist.estadoUsuario = 1
            db.session.commit()
            flash('Has confirmado tu correo correctamente', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ya has confirmado anteriormente tu correo electronico', 'info')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('auth.login'))

# Recuperar contraseña
@auth.route('/recuperar', methods=['GET', 'POST'])
def recuperarPass():
    if request.method == 'POST':
        emailUsuario = request.form['emailUser']
        
        usuarioData = Usuario.query.filter(Usuario.correoUsuario == emailUsuario).first()

        if usuarioData:
            msg = MIMEMultipart('alternative')

            contextMail = {
                'nombreUsuario' : usuarioData.nombreUsuario,
                'hash' : usuarioData.confirmationHash
            }

            file = render_template('mailForgotPassword.html', **contextMail )

            text = """\
            this is a recovery pass email
            If you dont see the button below
            Just press on the next link:
            localhost:5000/auth/recuperar/{}
            """.format(usuarioData.confirmationHash)

            msg['From']= 'david@mi.com.co'
            msg['To']= str(emailUsuario)
            msg['Subject']= "Recovery password MediFlow"

            part1 = MIMEText(text, "plain")
            part2 = MIMEText(file, "html")

            msg.attach(part1)
            msg.attach(part2)

            s.send_message(msg)

            flash('Si el correo existe se enviara un correo de recuperacion!', 'success')
            return redirect('/auth/login')
        else:
            flash('Si el correo existe se enviara un correo de recuperacion!', 'success')
            return redirect('/auth/login')

    return render_template('formForgotPassword.html')

@auth.route('/recuperar/<hash>', methods=['GET','POST'])
def recuperarPassCode(hash):
    uniqueHash = hash
    hashExist = Usuario.query.filter(Usuario.confirmationHash == uniqueHash).first()

    if hashExist:
        if 'emailUsuario' in session:
            session.pop('emailUsuario')
            session['emailUsuario'] = hashExist.correoUsuario
            return render_template('formResetPassword.html')
        else:
            session['emailUsuario'] = hashExist.correoUsuario
            return render_template('formResetPassword.html')

@auth.route('/changePass', methods=['POST'])
def cambiarPass():
    passwordUsuario = request.form['passwordUser']
    passwordUsuarioConfirm = request.form['passwordUserConfirm']

    

# Cerrar sesion
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))