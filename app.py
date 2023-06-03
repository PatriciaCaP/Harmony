from flask import Flask,  render_template, request, redirect, url_for, session, flash # pip install Flask
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from flask_paginate import Pagination, get_page_args
import datetime

from os import path #pip install notify-py
from notifypy import Notify
import MySQLdb.cursors
import random
import math


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'btug0fx7ljzszoqysnwl-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'up8pf5catvcodukz'
app.config['MYSQL_PASSWORD'] = 'wEo63IA2urQveLCLPiWl'
app.config['MYSQL_DB'] = 'btug0fx7ljzszoqysnwl'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)



########################## P R I N C I P A L ####################################
@app.route('/')
def home():
    frases = [
        "La música expresa lo que no puede decirse con palabras pero no puede permanecer en silencio. - Victor Hugo",
        "La música es el arte más directo, entra por el oído y va al corazón. - Magdalena Martínez",
        "La música es el corazón de la vida. Por ella habla el amor; sin ella no hay bien posible y con ella todo es hermoso. - Franz Liszt",
        "La música expresa lo que no puede decirse con palabras pero no puede permanecer en silencio. - Victor Hugo",
        "La música es el arte más directo, entra por el oído y va al corazón. - Magdalena Martínez",
        "La música es el corazón de la vida. Por ella habla el amor; sin ella no hay bien posible y con ella todo es hermoso. - Franz Liszt",
        "El arte es el perpetuo movimiento de la ilusión - Bob Dylan",
        "Dirás que soy un soñador, pero no soy el único - John Lenon",
        "La música es la medicina del alma. - Mick Jagger",
        "La música puede cambiar el mundo porque puede cambiar a las personas. - Bono",
        "La música es la forma en que puedo expresar mis emociones más intensas. - Eddie Vedder",
        "La música es una poderosa forma de comunicación. - Dave Grohl",
        "La música es el arte que está más cerca de las lágrimas y la memoria. - Steven Tyler",
        "La música es el idioma universal. - Shakira",
        "La música te lleva a un lugar donde siempre has querido estar. - John Mayer",
        "La música es mi religión. - Jimi Hendrix",
        "La música es el alimento del amor. - Elvis Presley",
        "La música es el único amor verdadero. - Jack White",

    
    ]
    frase_aleatoria = random.choice(frases)
    return render_template('principal.html', frase=frase_aleatoria)

@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("principal.html")

#########################################################################################################
#########################################################################################################

################################### L O G I N  Y  R E G I S T R O ###########################

# LOGIN
@app.route('/login', methods=["GET", "POST"])
def login():
    notificacion = Notify()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user is not None:
            if password == user["password"]:
                session['name'] = user['name']
                session['email'] = user['email']
                session['tipo'] = user['id_tip_usu']
                session['descripcion'] = user['descripcion']
                session['id'] = user['id']

                if session['tipo'] == 1:
                    return render_template("banda/home.html")
                elif session['tipo'] == 2:
                    return render_template("solista/homeTwo.html")
                elif session['name'] == "admin" and session['email'] == "admin@admin.com" and ['tipo'] == 3:
                    return render_template("admin.html")
                elif session['tipo'] == 3:
                    if session['name'] == 'admin' and session['email'] == 'admin@admin.com':
                       return render_template("admin.html")
                    else:
                       return render_template("ambos/homeThree.html")
                else:
                    notificacion.title = "Error de Acceso"
                    notificacion.message = "Tipo de usuario no válido"
                    notificacion.send()
                    return render_template("login.html")
            else:
                notificacion.title = "Error de Acceso"
                notificacion.message = "Correo o contraseña no válida"
                notificacion.send()
                return render_template("login.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message = "No existe el usuario"
            notificacion.send()
            return render_template("login.html")
    else:
        if 'email' in session:
            tipo = session['tipo']
            if tipo == 1:
                return render_template("banda/home.html")
            elif tipo == 2:
                return render_template("solista/homeTwo.html")
            
            elif tipo == 3:
                if session['name'] == "admin":
                    return render_template("admin.html")
                else:
                    return render_template("ambos/homeThree.html")
                
        return render_template("login.html")
 

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/registro', methods=["GET", "POST"])
def registro():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tip_usu")
    tipo = cur.fetchall()
    cur.close()

    notificacion = Notify()

    if request.method == 'GET':
        return render_template("registro.html", tipo=tipo)

    else:
        name = request.form['name']
        email = request.form['email']

        # Verificar si el nombre o correo electrónico ya existen en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE name = %s OR email = %s", (name, email))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            notificacion.title = "Registro Fallido"
            notificacion.message = "El nombre o correo electrónico ya está en uso"
            notificacion.send()
            return redirect(url_for('registro'))

        password = request.form['password']
        tip = request.form['tipo']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usuarios (name, email, password, id_tip_usu, descripcion) VALUES (%s,%s,%s,%s,%s)",
            (name, email, password, tip, descripcion))
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message = "Ya te encuentras registrado en Harmony, por favor inicia sesión y empieza a dar a conocer tu música"
        notificacion.send()
        return redirect(url_for('login'))
    
#############################################################################################################
#############################################################################################################

################################### P E R F I L E S ###########################################################

@app.route('/perfiles', methods=['GET', 'POST'])
def perfiles():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']

        # Ejecutar la consulta para obtener los perfiles de usuario por nombre
        cur.execute("SELECT name, email, id_tip_usu, descripcion FROM usuarios WHERE name LIKE %s", ('%' + name + '%',))
        usuarios = cur.fetchall()

    else:
        # Ejecutar la consulta para obtener todos los perfiles de usuario
        cur.execute("SELECT name, email, id_tip_usu, descripcion FROM usuarios")
        usuarios = cur.fetchall()
     

    cur.close()
    return render_template('perfiles.html', usuarios=usuarios)

@app.route('/perfil')
def perfil():
    if 'email' not in session:
        return redirect(url_for('login'))

    tipo = session['tipo']
    if tipo == 1:
        return render_template("banda/home.html")
    elif tipo == 2:
        return render_template("solista/homeTwo.html")
    elif tipo == 3:
        if session['name'] == 'admin' and session['email'] == 'admin@admin.com':
            return render_template("admin.html")
        else:
            return render_template("ambos/homeThree.html")
        
#########################################################################################################
#########################################################################################################
    
############################################### B L O G ######################################################
@app.route('/blogs')
def ver_blogs():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    cur = mysql.connection.cursor()
    
    # Consulta para obtener el número total de blogs
    cur.execute("SELECT COUNT(*) FROM blogs")
    result = cur.fetchone()
    total = result['COUNT(*)'] if result else 0
    
    # Consulta para obtener los blogs paginados
    cur.execute("SELECT blogs.id_blog, blogs.titulo, blogs.contenido, blogs.fecha, usuarios.name AS autor FROM blogs INNER JOIN usuarios ON blogs.id = usuarios.id ORDER BY blogs.fecha DESC LIMIT %s OFFSET %s", (per_page, offset))
    blogs = cur.fetchall()
    cur.close()

    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('blogs.html', blogs=blogs, pagination=pagination)



@app.route('/escribe_blog', methods=['GET', 'POST'])
def escribir_blog():
    notificacion = Notify()

    if 'email' not in session:
        return redirect(url_for('login'))

    id_usuario = session.get('id')

    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        id_usuario = session['id']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blogs (titulo, contenido, fecha, id) VALUES (%s, %s, NOW(), %s)", (titulo, contenido, id_usuario))
        mysql.connection.commit()

        notificacion.title = "Publicado con éxito"
        notificacion.message = "Has publicado en Harmony"
        notificacion.send()

        cur.close()

        return redirect(url_for('ver_blogs'))
    else:
        return render_template('create.html', id=id_usuario)


@app.route('/borrar_blog/<int:id_blog>', methods=['GET', 'POST'])
def borrar_blog(id_blog):
    cur = mysql.connection.cursor()

    # Obtener el autor del blog
    cur.execute("SELECT u.name as autor FROM blogs b JOIN usuarios u ON b.id = u.id WHERE b.id_blog = %s", (id_blog,))
    blog = cur.fetchone()

    if blog and blog['autor'] == session['name']:
        # Si el autor coincide con el usuario actual, se permite borrar el blog
        cur.execute("DELETE FROM blogs WHERE id_blog = %s", (id_blog,))
        mysql.connection.commit()
    elif 'name' in session and session['name'] == 'admin':
    # Si el usuario en la sesión es "admin", se permite borrar el blog
        cur.execute("DELETE FROM blogs WHERE id_blog = %s", (id_blog,))
        mysql.connection.commit()
    cur.close()

    return redirect(url_for('ver_blogs'))


@app.route('/editar_blog/<int:id_blog>', methods=['GET', 'POST'])
def editar_blog(id_blog):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        fecha = datetime.datetime.now()

        cur.execute("UPDATE blogs SET titulo = %s, contenido = %s, fecha = %s WHERE id_blog = %s",
                    (titulo, contenido, fecha, id_blog))
        mysql.connection.commit()

        flash('El blog ha sido actualizado exitosamente', 'success')

        cur.execute("SELECT * FROM blogs WHERE id_blog = %s", (id_blog,))
        blog = cur.fetchone()

        cur.close()

        return redirect(url_for('ver_blogs'))

    else:
        cur.execute("SELECT * FROM blogs WHERE id_blog = %s", (id_blog,))
        blog = cur.fetchone()
        cur.close()

        return render_template('editar_blog.html', blog=blog)
    

################################################################################################
################################################################################################    

######################## B O R R A R , E D I T A R  U S U A R I O S ############################

@app.route('/adminPerfiles')
def adminPerfiles():
    if 'name' in session and session['name'] == 'admin':
        cur = mysql.connection.cursor()

        # Obtener la lista de usuarios
        cur.execute("SELECT id, name, email, password, id_tip_usu, descripcion FROM usuarios")
        usuarios = cur.fetchall()

        cur.close()

        # Renderizar la plantilla perfiles.html y pasar la lista de usuarios como contexto
        return render_template('borrar_usuario.html', usuarios=usuarios)

    return 'Acceso no autorizado'

# Ruta para eliminar un usuario
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    if 'name' in session and session['name'] == 'admin':
        cur = mysql.connection.cursor()

        # Eliminar todos los valores del usuario de la base de datos
        cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        mysql.connection.commit()

        cur.close()

    return redirect(url_for('adminPerfiles'))

# Ruta para actualizar un usuario
@app.route('/actualizar_usuario/<int:id>', methods=['GET', 'POST'])
def actualizar_usuario(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        id_tip_usu = request.form['id_tip_usu']
        descripcion = request.form['descripcion']
       

        cur.execute("UPDATE usuarios SET name = %s, email = %s, id_tip_usu = %s , descripcion = %s WHERE id = %s",
                    (name, email, id_tip_usu, descripcion, id))
        mysql.connection.commit()

        flash('El usuario ha sido actualizado exitosamente', 'success')

        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cur.fetchone()

        cur.close()

        return redirect(url_for('adminPerfiles'))

    else:
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cur.fetchone()
        cur.close()

        return render_template('actualizar_usuario.html', usuario=usuario)


################################################################################################
################################################################################################

if __name__ == '__main__':
    app.secret_key = "clavedepatricia"
    app.run(debug=True)
