# importar librerias necesarias para la creación correcta de la base de datos
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Instanciar db y darle el varlor de la lib SQLAlchemy
db = SQLAlchemy()

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

    # Relaciones entre tablas
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario')) 

    # Definición de las relaciones 
    def __init__(self, nombreTask, descTurno, horaInicio, horaFin, idUsuarioFK):
        self.nombreTask = nombreTask
        self.descTurno = descTurno
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.idUsuarioFK = idUsuarioFK

# Definición de la clase Usuario mediante SQLAlchemy
class Usuario(UserMixin, db.Model):
    # Creación de la tabla Usuario
    __tablename__ = 'Usuario'
    # Declaración de columnas con sus respectivos tipos de dato
    idUsuario = db.Column(db.Integer, primary_key=True)
    correoUsuario = db.Column(db.String(45))
    contraseñaUsuario = db.Column(db.String(45))
    nombreUsuario = db.Column(db.String(45))
    apellidoUsuario = db.Column(db.String(45))
    telefonoUsuario = db.Column(db.String(10))
    numeroDocumento = db.Column(db.Integer)
    estadoUsuario = db.Column(db.Boolean(False))
    confirmationHash = db.Column(db.String(50))

    # Relaciones entre tablas
    idTipoDocumentoFK = db.Column(db.Integer, db.ForeignKey('TipoDocumento.idTipoDocumento'))
    idTipoUsuarioFK = db.Column(db.Integer, db.ForeignKey('TipoUsuario.idTipoUsuario'))
    especialidad_usuario = db.relationship('EspecialidadUsuario', back_populates="usuario")
    task = db.relationship('Task')

    def get_id(self):
        return (self.idUsuario)

    # Definición de las relaciones 
    def __init__(self, correoUsuario, contraseñaUsuario, nombreUsuario, apellidoUsuario, telefonoUsuario, numeroDocumento, estadoUsuario, idTipoDocumentoFK, idTipoUsuarioFK, confirmationHash):
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
    especialidad_usuario = db.relationship('EspecialidadUsuario', back_populates="especialidad")

    # Definición de las relaciones 
    def __init__(self, nombreEspecialidad):
        self.nombreEspecialidad = nombreEspecialidad

class EspecialidadUsuario(db.Model):
    # Creación de la tabla Usuario
    __tablename__ = 'EspecialidadUsuario'
    # Declaración de columnas con sus respectivos tipos de dato
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'), primary_key=True)
    idEspecialidad = db.Column(db.Integer, db.ForeignKey('Especialidad.idEspecialidad'), primary_key=True)
    descEspecialidad  = db.Column(db.String(255))

    # Relaciones entre tablas
    usuario = db.relationship('Usuario', back_populates="especialidad_usuario")
    especialidad = db.relationship('Especialidad', back_populates = "especialidad_usuario")

    # Definición de las relaciones 
    def __init__(self, idUsuario, idEspecialidad, descEspecialidad):
        self.idUsuario = idUsuario
        self.idEspecialidad = idEspecialidad
        self.descEspecialidad = descEspecialidad





        