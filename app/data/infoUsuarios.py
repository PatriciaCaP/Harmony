from flask import request

class Usuarios:
   def __init__(self, db):
      self.db = db

   def addUsuario(self, nombre,email,contraseña):
      if nombre and email and contraseña:
            cursor = self.db.cursor()
            sql = "INSERT INTO usuarios (nombre,email,contraseña) VALUES (%s,%s,%s)"
            data = (nombre,email,contraseña)
            cursor.execute(sql,data)
            self.db.commit()