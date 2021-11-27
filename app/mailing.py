import smtplib
import os

# Variables con los datos del correo
username = 'flowydomain@gmail.com'
password = os.getenv('MAIL_PASS', 'flowysi1')

# Conexion con servidor SMTP
s = smtplib.SMTP('smtp.gmail.com')
s.connect(host='smtp.gmail.com', port='587')
s.starttls()

s.login(username, password)