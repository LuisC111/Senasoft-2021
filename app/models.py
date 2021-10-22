# importar librerias necesarias para la creación correcta de la base de datos
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_marshmallow import Marshmallow


# Instanciar db y darle el varlor de la lib SQLAlchemy
db = SQLAlchemy()
ma = Marshmallow()

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class TipoUsuario(db.Model):
    # Creación de la tabla Usuario
    __tablename__ = 'TipoUsuario'
    # Declaración de columnas con sus respectivos tipos de dato
    idTipoUsuario = db.Column(db.Integer, primary_key=True)
    nombreTipoUsuario = db.Column(db.String(45))

    # Definición de las relaciones 
    def __init__(self, nombreTipoUsuario):
        self.nombreTipoUsuario = nombreTipoUsuario

class Task(db.Model):
    # Creación de la tabla Usuario
    __tablename__ = 'Task'
    # Declaración de columnas con sus respectivos tipos de dato
    idTask = db.Column(db.Integer, primary_key=True)
    nombreTask = db.Column(db.String(45))
    descTurno = db.Column(db.String(255))
    horaInicio = db.Column(db.DateTime)
    horaFin = db.Column(db.DateTime)
    urlReunion = db.Column(db.String(255))

    # Relaciones entre tablas
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario')) 
    idPacienteFK = db.Column(db.Integer, db.ForeignKey('Paciente.idPaciente'))
    # Definición de las relaciones 
    def __init__(self, nombreTask, descTurno, horaInicio, horaFin, urlReunion, idUsuarioFK,idPacienteFK):
        self.nombreTask = nombreTask
        self.descTurno = descTurno
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.urlReunion = urlReunion
        self.idUsuarioFK = idUsuarioFK
        self.idPacienteFK = idPacienteFK

    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'idTask'         : self.id,
           'nombreTask': self.nombreTask,
           'descTurno': self.descTurno,
           'descTurno': self.descTurno,
           'horaInicio': dump_datetime(self.horaInicio),
           'horaFin': dump_datetime(self.horaFin),
           'idPacienteFK' : self.idPacienteFK,
           'urlReunion': self.urlReunion,
       }

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True

class Paciente(db.Model):
    # Creación de la tabla Usuario
    __tablename__ = 'Paciente'
    # Declaración de columnas con sus respectivos tipos de dato
    idPaciente = db.Column(db.Integer, primary_key=True)
    nombrePaciente = db.Column(db.String(45))
    apellidoPaciente = db.Column(db.String(255))
    documentoPaciente = db.Column(db.String(45))
    telefonoPaciente = db.Column(db.String(45))
    estadoPaciente = db.Column(db.Boolean(False))
    edadPaciente = db.Column(db.Integer)
    # Relaciones entre tablas
    idEspecialidadFK = db.Column(db.Integer, db.ForeignKey('Especialidad.idEspecialidad'))
    task = db.relationship('Task')

    # Definición de las relaciones 
    def __init__(self, nombrePaciente, apellidoPaciente, documentoPaciente, telefonoPaciente, estadoPaciente, edadPaciente, idEspecialidadFK):
        self.nombrePaciente = nombrePaciente
        self.apellidoPaciente = apellidoPaciente
        self.documentoPaciente = documentoPaciente
        self.telefonoPaciente = telefonoPaciente
        self.estadoPaciente = estadoPaciente
        self.edadPaciente = edadPaciente
        self.idEspecialidadFK = idEspecialidadFK

# Definición de la clase Usuario mediante SQLAlchemy
class Usuario(UserMixin, db.Model):
    # Creación de la tabla Usuario
    __tablename__ = 'Usuario'
    # Declaración de columnas con sus respectivos tipos de dato
    idUsuario = db.Column(db.Integer, primary_key=True)
    correoUsuario = db.Column(db.String(45), unique=True)
    contraseñaUsuario = db.Column(db.String(45))
    nombreUsuario = db.Column(db.String(45))
    apellidoUsuario = db.Column(db.String(45))
    telefonoUsuario = db.Column(db.String(10))
    numeroDocumento = db.Column(db.String(15))
    estadoUsuario = db.Column(db.Boolean(False))
    confirmationHash = db.Column(db.String(50))

    # Relaciones entre tablas
    idTipoDocumentoFK = db.Column(db.Integer, db.ForeignKey('TipoDocumento.idTipoDocumento'))
    idTipoUsuarioFK = db.Column(db.Integer, db.ForeignKey('TipoUsuario.idTipoUsuario'))
    idEspecialidadFK = db.Column(db.Integer, db.ForeignKey('Especialidad.idEspecialidad'))
    task = db.relationship('Task')

    def get_id(self):
        return (self.idUsuario)

    # Definición de las relaciones 
    def __init__(self, correoUsuario, contraseñaUsuario, nombreUsuario, apellidoUsuario, telefonoUsuario, numeroDocumento, estadoUsuario, idTipoDocumentoFK, idTipoUsuarioFK, confirmationHash, idEspecialidadFK):
        self.correoUsuario = correoUsuario
        self.contraseñaUsuario = contraseñaUsuario
        self.nombreUsuario = nombreUsuario
        self.apellidoUsuario = apellidoUsuario
        self.telefonoUsuario = telefonoUsuario
        self.numeroDocumento = numeroDocumento
        self.estadoUsuario = estadoUsuario
        self.idTipoDocumentoFK = idTipoDocumentoFK
        self.idTipoUsuarioFK = idTipoUsuarioFK
        self.confirmationHash = confirmationHash
        self.idEspecialidadFK = idEspecialidadFK
# Definición de la clase TipoDocumento mediante SQLAlchemy
class TipoDocumento(db.Model):
    # Creacion de la tabla TipoDocumento
    __tablename__ = 'TipoDocumento'
    # Declaración de columnas con sus respectivos tipos de dato
    idTipoDocumento = db.Column(db.Integer, primary_key=True)
    nombreTipoDocumento = db.Column(db.String(45))

    # Relaciones entre tablas
    usuarioDocumento = db.relationship('Usuario')
    
    # Creacion contructor Tabla
    def __init__(self, nombreTipoDocumento):
        self.nombreTipoDocumento = nombreTipoDocumento

class Especialidad(db.Model):
    # Creación de la tabla Usuario
    __tablename__ = 'Especialidad'
    # Declaración de columnas con sus respectivos tipos de dato
    idEspecialidad = db.Column(db.Integer, primary_key=True)
    nombreEspecialidad = db.Column(db.String(45))

    # Relaciones entre tablas
    usuario = db.relationship('Usuario')
    paciente = db.relationship('Paciente')

    # Definición de las relaciones 
    def __init__(self, nombreEspecialidad):
        self.nombreEspecialidad = nombreEspecialidad
