# importar librerias necesarias para la creación correcta de la base de datos
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Instanciar db y darle el varlor de la lib SQLAlchemy
db = SQLAlchemy()

# Definición de la clase Usuario mediante SQLAlchemy
class Usuario(db.Model):
    # Creación de la tabla Usuario
    __tablename__ = 'Usuario'
    # Declaración de columnas con sus respectivos tipos de dato
    idUsuario = db.Column(db.Integer, primary_key=True)
    correoUsuario = db.Column(db.String(45))
    contraseñaUsuario = db.Column(db.String(45))
    nombreUsuario = db.Column(db.String(45))
    apellidoUsuario = db.Column(db.String(45))
    telefonoUsuario = db.Column(db.Integer(10))
    numeroDocumento = db.Column(db.Integer(45))
    estadoUsuario = db.Column(db.Boolean(False))

    # Relaciones entre tablas
    idTipoDocumentoFK = db.Column(db.Integer, db.ForeignKey('TipoDocumento.idTipoDocumento'))
    idTaskFK = db.Column(db.Integer, db.ForeignKey('Task.idTask'))
    idTipoUsuarioFK = db.Column(db.Integer, db.ForeignKey('TipoUsuario.idTipoDocumento'))

    # Definición de las relaciones 
    def __init__(self, correoUsuario, contraseñaUsuario, nombreUsuario, apellidoUsuario, telefonoUsuario, numeroDocumento, estadoUsuario, idTipoDocumentoFK, idTaskFK, idTipoUsuarioFK):
        self.correoUsuario = correoUsuario
        self.contraseñaUsuario = contraseñaUsuario
        self.nombreUsuario = apellidoUsuario
        self.apellidoUsuario = apellidoUsuario
        self.telefonoUsuario = telefonoUsuario
        self.numeroDocumento = numeroDocumento
        self.estadoUsuario = estadoUsuario
        self.idTipoDocumentoFK = idTipoDocumentoFK
        self.idTaskFK = idTaskFK
        self.idTipoUsuarioFK = idTipoUsuarioFK
        