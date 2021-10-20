# importar app con todos sus configuraciones
from app import create_app

# Importar toda la base de datos
from app.models import db, TipoDocumento, Usuario, Especialidad, Task, TipoUsuario, EspecialidadUsuario

# Creacion de la base de datos
app=create_app()
app.app_context().push()
db.create_all()

# Insersion de datos 
tipoDoc1 = TipoDocumento('Cedula Ciudadania')
tipoDoc2 = TipoDocumento('Tarjeta de Identidad')
tipoDoc3 = TipoDocumento('Pasaporte')

TipoUsuario1 = TipoUsuario('Administrador')
TipoUsuario2 = TipoUsuario('Encargado')
TipoUsuario3 = TipoUsuario('Empleados')

especialidad1 = Especialidad('Pediatra')
especialidad2 = Especialidad('Optometra')
especialidad3 = Especialidad('Medico General') 

Task1 = Task('Consultorio Pediatria piso 1','Atender el consultorio de pediatria en el turno de la mañana','2021-01-03 11:30:00','2021-01-03 13:30:00', 5)
Task2 = Task('Consultorio Pediatria piso 1','Atender el consultorio de pediatria en el turno de la mañana','2021-01-03 14:00:00','2021-01-03 16:00:00', 6)
Task3 = Task('Consultorio 3 piso 1','Atender el consultorio 3 en el turno de la mañana','2021-01-06 06:00:00','2021-01-06 10:00:00', 5)
Task4 = Task('Consultorio 3 piso 1','Atender el consultorio 3 en el turno de la tarde','2021-01-06 12:00:00','2021-01-06 14:00:00', 5)
Task5 = Task('Consultorio 1 piso 2','Atender el consultorio 1 en el turno de la tarde','2021-01-09 14:00:00','2021-01-09 18:00:00', 6)
Task6 = Task('Consultorio 1 piso 2','Atender el consultorio 1 en el turno de la noche','2021-01-09 18:30:00','2021-01-09 22:30:00', 6)

usuario1 = Usuario('hectorflorez25@gmail.com', '12345678', 'Hector', 'Florez', '3162943432', '1000622639', 1, 1, 1, None)
usuario2 = Usuario('hectorflorez35@gmail.com', '12345678', 'Jesid', 'Florez', '3162943432', '1002114522', 1, 1, 1, None)
usuario3 = Usuario('hjflorez93@misena.edu.co', '12345678', 'Luis', 'Carlos', '3162943432', '1236925233', 1, 1, 2, None)
usuario4 = Usuario('pep01@gmail.com', '12345678', 'Pepe', 'Perez', '3162943432', '1478523698', 1, 1, 2, None)
usuario5 = Usuario('prueba12@gmail.com', '12345678', 'Prueba', 'Sena', '3162943432', '1695325698', 1, 1, 3, None)
usuario6 = Usuario('micorreo123@gmail.com', '12345678', 'Lucho', 'Paez', '3162943432', '1003365995', 1, 1, 3, None)


especialidadUsu1 = EspecialidadUsuario(5,1,'Pediatra')
especialidadUsu2 = EspecialidadUsuario(6,2,'Optometra especializado')

# Envio de datos a la bd
db.session.add(tipoDoc1)
db.session.add(tipoDoc2)
db.session.add(tipoDoc3)
db.session.add(TipoUsuario1)
db.session.add(TipoUsuario2)
db.session.add(TipoUsuario3)
db.session.add(especialidad1)
db.session.add(especialidad2)
db.session.add(especialidad3)
db.session.add(Task1)
db.session.add(Task2)
db.session.add(Task3)
db.session.add(Task4)
db.session.add(Task5)
db.session.add(Task6)
db.session.add(usuario1)
db.session.add(usuario2)
db.session.add(usuario3)
db.session.add(usuario4)
db.session.add(usuario5)
db.session.add(usuario6)
db.session.add(especialidadUsu1)
db.session.add(especialidadUsu2)
db.session.commit()

