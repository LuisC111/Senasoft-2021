from flask import redirect, url_for, render_template, flash, request
from . import panel
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
from ..models import Usuario, TipoUsuario, db
from functools import wraps
from ..auth.views import login_manager
import uuid

@login_manager.user_loader
def load_user(user_id):
    try:
        return Usuario.query.get(user_id)
    except:
        return None

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.idTipoUsuarioFK == 1:
            return f(*args, **kwargs)
        else:
            flash('Necesitas ser administrador para ver esta pagina', 'info')
            return redirect(url_for('panel.panelInicio'))

    return wrap

def employ_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.idTipoUsuario == 2:
            return f(*args, **kwargs)
        else:
            flash('Necesitas ser un encargado para mirar esta pagina', 'info')
            return redirect(url_for('panel.panelInicio'))

    return wrap

@panel.route('/')
@login_required
def panelInicio():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    return render_template('panelUsuario.html', **context)

@panel.route('/calendar')
@login_required
def panelCalendar():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }
    return render_template('panelCalendar.html', **context)

@panel.route('/usuarios')
#@admin_required
@login_required
def panelUsuarios():
    all_data = Usuario.query.filter(Usuario.estadoUsuario == 1).all()
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user,
        'usuarios' : all_data
    }

    return render_template('datatablesPanelUsuario.html', **context)

@panel.route('/turnos')
@login_required
def panelTurnos():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    return render_template('datatablesPanelTurnos.html', **context )

@panel.route('/especialidades')
@login_required
def panelEsp():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    return render_template('datatablesPanelEspecialidades.html', **context)

@panel.route('/paciente')
@login_required
def panelPaciente():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    return render_template('datatablesPaciente.html', **context)

@panel.route('/crearUsuario', methods=['GET', 'POST'])
@login_required
def panelCrear():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    if request.method == 'POST':
        nombreUsuario = request.form['nombreUsuario']
        apellidoUsuario = request.form['apellidoUsuario']
        correoUsuario = request.form['correoUsuario']
        passwordUsuario = request.form['passwordUsuario']
        telefonoUsuario = request.form['telefonoUsuario']
        documentoUsuario = request.form['documentoUsuario']
        tipoDocumento = request.form.get('tipoDocumento')
        tipoUsuario = request.form.get('tipoUsuario')
        confirmationHash = str(uuid.uuid4().hex)

        # Busqueda en base de datos si el usuario existe
        usuarioData = Usuario.query.filter(Usuario.correoUsuario == correoUsuario).first()

        if usuarioData:
            flash('Este correo ya se encuentra registrado!', 'error')
        else:
            newUsuario = Usuario(correoUsuario, passwordUsuario, nombreUsuario, apellidoUsuario, telefonoUsuario, documentoUsuario, 1, tipoDocumento, tipoUsuario, confirmationHash)

            db.session.add(newUsuario)
            db.session.commit()
            
            flash('Usuario creado correctamente', 'success')

            return redirect(url_for('panel.panelUsuarios'))

    return render_template('crearUsuario.html', **context)


@panel.route('/crearPaciente', methods=['GET', 'POST'])
@login_required
def panelCrearPaciente():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    return render_template('datatablesPaciente.html', **context)

@panel.route('/crearTurno', methods=['GET', 'POST'])
@login_required
def panelCrearTurno():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    return render_template('datatablesPaciente.html', **context)

@panel.route('/editarPerfil/<userId>', methods=['GET', 'POST'])
@login_required
def panelEditar(userId):
    
    if request.method == 'POST':
        nombre = request.form['nombreUsuario']
        apellido = request.form['apellidoUsuario']
        correo = request.form['correoUsuario']
        telefono = request.form['datTelefono']
        numDoc = request.form['documentoUsuario']

        
        datosPerfilUsuario = Usuario.query.filter(Usuario.idUsuario == userId).first()
        datosPerfilUsuario.nombreUsuario = nombre
        datosPerfilUsuario.apellidoUsuario = apellido
        datosPerfilUsuario.correoUsuario = correo
        datosPerfilUsuario.telefonoUsuario = telefono
        datosPerfilUsuario.numeroDocumento = numDoc
        
        db.session.add(datosPerfilUsuario)
        db.session.commit()

        flash('Datos actualizados correctamente', 'success')
        return redirect("/panel/editarPerfil/"+userId) 

    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    return render_template('editarPerfilUsuario.html', **context)

