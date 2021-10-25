#Creacion de configuraciones globales del proyecto
class Config():
    SECRET_KEY = 'ASDGHJKLDFGHJK'
    SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://root:root@mysqldb/SenaSoft' #Conexion con db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_EMAIL_SENDER = 'flowydomain@gmail.com'


