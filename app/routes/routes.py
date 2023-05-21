from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash # pip install Flask
from app import db

from app.data.infoUsuarios import Usuarios

app = Blueprint("routes", __name__)

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("login.html")

@app.route("/logout")
def logout():
	session["nombre"] = None
	return redirect("/contenido")

@app.route("/contenido")
def index():
  # check if the users exist or not
    if not session.get("nombre"):
        # if not there in the session then redirect to the login page
        return redirect("/")
    return render_template('contenido.html')


@app.route("/registrarse" , methods=["POST"])
def registrarse():
    nombre = request.form['nombre'] # PARA PODER OBTENER EL CONTENIDO DEL INPUT CON EL NOMBRE QUE INDIQUEMOS
    email = request.form['email'] # PARA PODER OBTENER EL CONTENIDO DEL INPUT CON EL NOMBRE QUE INDIQUEMOS
    contraseña = request.form['contraseña'] # PARA PODER OBTENER EL CONTENIDO DEL INPUT CON EL NOMBRE QUE INDIQUEMOS
    infoUsuarios : Usuarios = Usuarios(db)
    infoUsuarios.addUsuario(nombre,email,contraseña)
    return redirect(url_for('routes.registrado')) # Y REDIRIGIMOS A HOME DE NUE
  
@app.route('/registrado', methods=["POST", "GET"])
def registrado():
    return render_template("registrado.html")