from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector  # IMPORTAMOS LO QUE HEMOS INSTALADO PIP INSTALL MYSQL.......

#db = list()
db = mysql.connector.connect( # LLAMAMOS AL FUNCION CONNECT PARA CONECTARNOS
    host ='bqxo2nyaltlkfb7xfuft-mysql.services.clever-cloud.com', #NUESTRO HOST, ESTA EN EL DOCKER COMPOSE
    port = 3306,
    user ='uzb8hewphwelnsnw', #USUARIO QUE USAMOS NOSOTROS
    password ='YelZ440RYDQGLOlx4leb', #CONTRASEÑA CON LA QUE NOS CONECTAMOS
    database='bqxo2nyaltlkfb7xfuft'
) 

def create_app():
    app = Flask(__name__)
    app.debug = True
    
    from .routes import routes

    app.register_blueprint(routes.app)

    return app
