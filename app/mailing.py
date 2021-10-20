import smtplib
import os

username = 'flowydomain@gmail.com'
password = 'flowysi1'
# file = codecs.open("index.html", "r", "utf-8")

s = smtplib.SMTP('smtp.gmail.com')
s.connect(host='smtp.gmail.com', port='587')
s.starttls()
s.login(username, password)