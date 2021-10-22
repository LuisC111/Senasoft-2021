from flask import redirect, url_for, render_template, flash, request, jsonify, Response
from . import panel
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
from ..models import Usuario, TipoUsuario, TipoDocumento, db, Paciente, Task, TaskSchema, Especialidad
from functools import wraps
from ..auth.views import login_manager
import json
from fpdf import FPDF
import uuid
import jsonpickle
from flask_cors import CORS, cross_origin

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

@panel.route('/calendar', methods=['GET', 'POST'])
@login_required
def panelCalendar():
    all_enfermeras = Usuario.query.filter(Usuario.estadoUsuario == 1, Usuario.idTipoUsuarioFK == 3).all()
    taskEnfermeras = Task.query.all

    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user,
        'enfermeras' : all_enfermeras,
        'taks' : taskEnfermeras
    }
          
    return render_template('panelCalendar.html', **context)

@panel.route('/calendar/<int:idUsuario>', methods=['GET', 'POST'])
@login_required
def panelCalendarUsuario(idUsuario):
    
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user,
        'enfermeraSeleccionada' : idUsuario
    }
          
    return render_template('panelCalendar.html', **context)

@panel.route('/calendar/jsonfile/<userId>')
@cross_origin(supports_credentials=True)
@login_required
def jsonfile(userId):
    taskData = Task.query.filter(Task.idUsuarioFK == userId).all()
    task_Schema = TaskSchema(many=True)
    output = task_Schema.dump(taskData)

    return jsonify(output)

@panel.route('/calendar/nuevoCalendar/<int:idUsuario>', methods=['GET', 'POST'])
@login_required
def panelCalendarNuevo(idUsuario):
    if request.method == 'POST':
        idUsuarioActual = request.form['idUsuario']
        nombreTask = request.form['nombreTask']
        describcionTaks = "prueba"
        fechaInicio = request.form['fechaInicio']
        fechaFin = request.form['fechaFin']
        pacienteId = request.form['idPaciente']
        newTask = Task(nombreTask, describcionTaks, fechaInicio, fechaFin, None, idUsuario, int(pacienteId))
        # nombreTask, descTurno, horaInicio, horaFin, urlReunion, idUsuarioFK,idPacienteFK

        db.session.add(newTask)
        db.session.commit()

        usuarioId = newTask.idUsuarioFK

        dataAllUsuario = Task.query.filter(Task.idUsuarioFK == usuarioId).all()
        
        dataUsuario = []
        fechasUsuario = []

        for data in dataAllUsuario:
            dataUsuario.append(data)
        
        for data in dataUsuario:
            onlyDate = data.horaInicio
            fechasUsuario.append(onlyDate)
        
        horasTotal = 0
        
        flash('Tarea creada correctamente', 'success')
        
        return redirect(url_for('panel.panelCalendarUsuario', idUsuario=idUsuarioActual))

@panel.route('/calendar/eliminar/<int:idCalendar>', methods=['GET', 'POST'])
@login_required
def panelCalendarEliminar(idCalendar):
    if request.method == 'POST':
        dataTask = Task.query.filter(Task.idTask == idCalendar).first()
        idUsuarioActual = request.form['idUsuario']

        db.session.delete(dataTask)
        db.session.commit()

        flash('Tarea eliminada correctamente', 'success')
        
        return redirect(url_for('panel.panelCalendarUsuario', idUsuario=idUsuarioActual))

@panel.route('/calendar/editar/<int:idCalendar>', methods=['POST'])
@login_required
def panelCalendarEditar(idCalendar):
    if request.method == 'POST':
        dataTask = Task.query.filter(Task.idTask == idCalendar).first()
        idUsuarioActual = request.form['idUsuario']

        nombreTask = request.form['nombreTask']
        fechaInicio = request.form['fechaInicio']
        print(fechaInicio)
       
        fechaFin = request.form['fechaFin']
        
        dataTask.nombreTask = nombreTask
        dataTask.horaInicio = fechaInicio
        dataTask.horaFin = fechaFin

        db.session.commit()

        flash('Tarea editada correctamente', 'success')
        
        return redirect(url_for('panel.panelCalendarUsuario', idUsuario=idUsuarioActual))

@panel.route('/usuarios')
@admin_required
@login_required
def panelUsuarios():
    all_data = Usuario.query.filter(Usuario.estadoUsuario == 1).all()
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'apellidoUsuario' : current_user.apellidoUsuario,
        'userLogged' : current_user,
        'usuarios' : all_data
    }

    return render_template('datatablesPanelUsuario.html', **context)

@panel.route('usuarios/crearUsuario', methods=['GET', 'POST'])
@admin_required
@login_required
def panelCrearUsuario():
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
        tipoEspecialidad = int(request.form.get('tipoEspecialidad'))
        confirmationHash = str(uuid.uuid4().hex)

        # Busqueda en base de datos si el usuario existe
        usuarioData = Usuario.query.filter(Usuario.correoUsuario == correoUsuario).first()

        if usuarioData:
            flash('Este correo ya se encuentra registrado!', 'error')
        else:
            if tipoUsuario == 3 or tipoUsuario == '3':
                newUsuario = Usuario(correoUsuario, passwordUsuario, nombreUsuario, apellidoUsuario, telefonoUsuario, documentoUsuario, 1, tipoDocumento, tipoUsuario, confirmationHash, tipoEspecialidad)

                db.session.add(newUsuario)
                db.session.commit()
                
                flash('Usuario creado correctamente', 'success')

                return redirect(url_for('panel.panelUsuarios'))
            else:
                newUsuario = Usuario(correoUsuario, passwordUsuario, nombreUsuario, apellidoUsuario, telefonoUsuario, documentoUsuario, 1, tipoDocumento, tipoUsuario, confirmationHash, None)

                db.session.add(newUsuario)
                db.session.commit()
                
                flash('Usuario creado correctamente', 'success')

                return redirect(url_for('panel.panelUsuarios'))

    return render_template('crearUsuario.html', **context)

@panel.route('/usuarios/inactivar/<int:idUsuario>', methods=['GET', 'POST'])
@admin_required
@login_required
def inactivarUsuario(idUsuario):
    usuarioIdURL = idUsuario
    usuarioData = Usuario.query.filter(Usuario.idUsuario == usuarioIdURL).first()

    if usuarioData:
        if usuarioData.estadoUsuario == 1:
            usuarioData.estadoUsuario = 0
            db.session.commit()
            flash('Usuario inactivado correctamente', 'success')

            return redirect(url_for('panel.panelUsuarios'))
        else:
            flash('Usuario ya se encuentra inactivo', 'info')
            return redirect(url_for('panel.panelUsuarios'))
    else:
        flash('Error, usuario no existe', 'info')
        return redirect(url_for('panel.panelUsuarios'))

@panel.route('/usuarios/editarUsuario/<int:idUsuario>', methods=['GET', 'POST'])
@admin_required
@login_required
def editarUsuario(idUsuario):
    all_data = Usuario.query.filter(Usuario.estadoUsuario == 1).all()

    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user,
        'usuarios' : all_data
    }

    usuarioIdURL = idUsuario
    usuarioData = Usuario.query.filter(Usuario.idUsuario == usuarioIdURL).first()

    if usuarioData:
        context['UsuarioData'] = usuarioData

    if request.method == 'POST':
        nombreUsuario = request.form['nombreUsuario']
        apellidoUsuario = request.form['apellidoUsuario']
        correoUsuario = request.form['emailUsuario']
        passwordUsuario = usuarioData.contraseñaUsuario
        telefonoUsuario = request.form['telefonoUsuario']
        documentoUsuario = request.form['documentoUsuario']
        tipoDocumento = request.form.get('tipoDocumento')
        tipoUsuario = request.form.get('tipoUsuario')
        tipoEspecialidad = request.form.get('tipoEspecialidad')

        usuarioData.nombreUsuario = nombreUsuario
        usuarioData.apellidoUsuario = apellidoUsuario
        usuarioData.correoUsuario = correoUsuario
        usuarioData.telefonoUsuario = telefonoUsuario
        usuarioData.numeroDocumento = documentoUsuario
        usuarioData.idTipoDocumentoFK = tipoDocumento
        usuarioData.idTipoUsuarioFK = tipoUsuario
        usuarioData.idEspecialidadFK = tipoEspecialidad

        db.session.commit()

        flash('Usuario editado correctamente', 'success')
        return redirect(url_for('panel.panelUsuarios'))

    return render_template('datatablesPanelUsuario.html', **context)

@panel.route('/pacientes')
@login_required
def panelPaciente():
    all_data = Paciente.query.filter(Paciente.estadoPaciente == 1).all()

    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user,
        'pacientes' : all_data
    }

    return render_template('datatablesPaciente.html', **context)

@panel.route('/paciente/crearPaciente', methods=['GET', 'POST'])
@login_required
def panelCrearPaciente():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    if request.method == 'POST':
        nombrePaciente = request.form['nombrePaciente']
        apellidoPaciente = request.form['apellidoPaciente']
        documentoPaciente = request.form['documentoPaciente']
        telefonoPaciente = request.form['telefonoPaciente']
        edadPaciente = request.form['edadPaciente']
        especialidadPaciente = request.form.get('especialidadPaciente')

        newPaciente = Paciente(nombrePaciente, apellidoPaciente, documentoPaciente, telefonoPaciente, 1, edadPaciente, especialidadPaciente)
        # nombrePaciente, apellidoPaciente, documentoPaciente, telefonoPaciente, estadoPaciente, edadPaciente, idEspecialidadFK
        
        db.session.add(newPaciente)
        db.session.commit()

        flash('Se ha creado un nuevo paciente correctamente', 'success')

        return redirect(url_for('panel.panelPaciente'))

    return render_template('crearPaciente.html', **context)

@panel.route('/paciente/editarPaciente/<int:idPaciente>', methods=['GET', 'POST'])
@login_required
def editarPaciente(idPaciente):
    all_data = Paciente.query.filter(Paciente.estadoPaciente == 1).all()

    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user,
        'pacientes' : all_data
    }

    usuarioIdURL = idPaciente
    pacienteData = Paciente.query.filter(Paciente.idPaciente == usuarioIdURL).first()

    if pacienteData:
        context['PacienteData'] = pacienteData
    else:
        flash('no hay paciente data', 'error')

    if request.method == 'POST':
        nombreUsuario = request.form['nombreUsuario']
        apellidoUsuario = request.form['apellidoUsuario']
        telefonoUsuario = request.form['telefonoUsuario']
        documentoUsuario = request.form['documentoUsuario']
        edadUsuario = request.form['edadUsuario']
        especialidadUsuario = request.form.get('especialidadUsuario')

        pacienteData.nombrePaciente = nombreUsuario
        pacienteData.apellidoPaciente = apellidoUsuario
        pacienteData.telefonoPaciente = telefonoUsuario
        pacienteData.documentoPaciente = documentoUsuario
        pacienteData.edadPaciente = edadUsuario
        pacienteData.idEspecialidadFK = especialidadUsuario

        db.session.commit()

        flash('Paciente editado correctamente', 'success')
        return redirect(url_for('panel.panelPaciente'))

    return render_template('datatablesPaciente.html', **context)

@panel.route('/paciente/inactivar/<int:idPaciente>')
@login_required
def inactivarPacientePanel(idPaciente):
    usuarioIdURL = idPaciente
    usuarioData = Paciente.query.filter(Paciente.idPaciente == usuarioIdURL).first()

    if usuarioData:
        if usuarioData.estadoPaciente == 1:
            usuarioData.estadoPaciente = 0
            db.session.commit()
            flash('Paciente inactivado correctamente', 'success')

            return redirect(url_for('panel.panelPaciente'))
        else:
            flash('paciente ya se encuentra inactivo', 'info')
            return redirect(url_for('panel.panelPaciente'))
    else:
        flash('Error, paciente no existe', 'info')
        return redirect(url_for('panel.panelPaciente'))

@panel.route('/turnos')
@login_required
def panelTurnos():
    all_data = Task.query.all()
    all_Usuario = Usuario.query.all()
    all_Paciente = Paciente.query.all()

    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user,
        'turnos' : all_data,
        'usuarios' : all_Usuario,
        'pacientes' : all_Paciente,
    }

    return render_template('datatablesPanelTurnos.html', **context )

"""@panel.route('/turno/crearturno', methods=['GET', 'POST'])
@login_required
def panelCrearTurno():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    if request.method == 'POST':
        nombreTurno = request.form['nombreTurno']
        descripcionTurno = request.form['descripcionTurno']
        fechaInicio = request.form['fechaInicio']
        edadUsuario = request.form['edadUsuario']
        edadUsuario = request.form['edadUsuario']
        edadUsuario = request.form['edadUsuario']

    return render_template('crearTurno.html', **context)"""

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
