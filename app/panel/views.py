from flask import redirect, url_for, render_template, flash, request, jsonify, Response
from . import panel
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
from ..models import Usuario, TipoUsuario, db, Paciente, Task, TaskSchema, Especialidad
from functools import wraps
from ..auth.views import login_manager
import json
from fpdf import FPDF
import uuid
import jsonpickle

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

@panel.route('/calendar/jsonfile')
@login_required
def jsonfile():
    taskData = Task.query.all()
    task_Schema = TaskSchema(many=True)
    output = task_Schema.dump(taskData)

    return jsonify({'data' : output})

@panel.route('/usuarios')
#@admin_required
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
        tipoEspecialidad = request.form.get('tipoEspecialidad')
        confirmationHash = str(uuid.uuid4().hex)

        # Busqueda en base de datos si el usuario existe
        usuarioData = Usuario.query.filter(Usuario.correoUsuario == correoUsuario).first()

        if usuarioData:
            flash('Este correo ya se encuentra registrado!', 'error')
        else:
            if tipoEspecialidad == 1 or tipoEspecialidad == 2 or tipoEspecialidad == 3 or tipoEspecialidad ==4:
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

    return render_template('datatablesPaciente.html', **context)

@panel.route('/turnos')
@login_required
def panelTurnos():
    all_data = Task.query.all()
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user,
        'turnos' : all_data
    }

    return render_template('datatablesPanelTurnos.html', **context )

@panel.route('/crearTurno', methods=['GET', 'POST'])
@login_required
def panelCrearTurno():
    context = {
        'nombreUsuario' : current_user.nombreUsuario,
        'userLogged' : current_user
    }

    return render_template('datatablesPanelTurnos.html', **context)

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

@panel.route('/reporte/pdf', methods=['GET', 'POST'])
@login_required
def download_report ():
    dataUsuario = db.session.query(Usuario,TipoDocumento,TipoUsuario,Especialidad).outerjoin(TipoDocumento,TipoUsuario,Especialidad).all()
    
    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width/8
        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Reporte vehiculos', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)
    pdf.cell(col_width, pdf.font_size, 'Placa', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Modelo', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Marca', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Estado', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Precio', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Nombre', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Apellido', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Categoria',border=1, ln=0, align='C', fill=0)
        
    pdf.ln(4)
        
    th = pdf.font_size
    pdf.set_font('Courier', '', 12)
    for row, row2, row3 in datosVehiculos:
        pdf.cell(col_width, th, str(row.vehPlaca), border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row.vehModelo), border=1, ln=0, align='C')
        pdf.cell(col_width, th, row.vehMarca, border=1, ln=0, align='C')
        pdf.cell(col_width, th, row.vehEstado, border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row.vehPrecio), border=1, ln=0, align='C')
        pdf.cell(col_width, th, row3.datNombre, border=1, ln=0, align='C')
        pdf.cell(col_width, th, row3.datApellido, border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row2.catTipo), border=1, ln=0, align='C')
        pdf.ln(th)
        
    pdf.ln(10)
        
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- Fin reporte -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=vendedor_report.pdf'})