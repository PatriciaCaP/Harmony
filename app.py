from flask import Flask,  render_template, request, redirect, url_for, session, flash # pip install Flask
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from flask_paginate import Pagination, get_page_args
from os import path #pip install notify-py
from notifypy import Notify
import datetime
import random



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
    frase_aleatoria = random.choice(frases) # La función random.choice() selecciona una frase al azar de la lista.
    return render_template('principal.html', frase=frase_aleatoria)

@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("principal.html")

#########################################################################################################
#########################################################################################################

################################### L O G I N  Y  R E G I S T R O ###########################

# LOGIN
@app.route('/login', methods=["GET", "POST"])  # Ruta '/login' que acepta solicitudes GET y POST
def login():
    notificacion = Notify()  # Creación de una instancia de la clase Notify para enviar notificaciones

    if request.method == 'POST':  # Si la solicitud es de tipo POST (se envió un formulario)
        email = request.form['email']  # Obtención del correo electrónico del formulario
        password = request.form['password']  # Obtención de la contraseña del formulario

        cur = mysql.connection.cursor()  # Creación de un cursor para ejecutar consultas en la base de datos
        cur.execute("SELECT * FROM usuarios WHERE email=%s", (email,))  # Consulta para obtener el usuario con el correo electrónico ingresado
        user = cur.fetchone()  # Obtiene el primer resultado de la consulta
        cur.close()  # Cierre del cursor

        if user is not None:  # Si se encontró un usuario con el correo electrónico proporcionado
            if password == user["password"]:  # Si la contraseña ingresada coincide con la contraseña almacenada
                session['name'] = user['name']  # Se establece la variable de sesión 'name' con el nombre del usuario
                session['email'] = user['email']  # Se establece la variable de sesión 'email' con el correo electrónico del usuario
                session['tipo'] = user['id_tip_usu']  # Se establece la variable de sesión 'tipo' con el tipo de usuario
                session['descripcion'] = user['descripcion']  # Se establece la variable de sesión 'descripcion' con la descripción del usuario
                session['id'] = user['id']  # Se establece la variable de sesión 'id' con el ID del usuario

                if session['tipo'] == 1:  # Si el tipo de usuario es 1 (banda)
                    return render_template("perfiles/banda/home.html")  # Renderiza la plantilla para el perfil de la banda
                elif session['tipo'] == 2:  # Si el tipo de usuario es 2 (solista)
                    return render_template("perfiles/solista/homeTwo.html")  # Renderiza la plantilla para el perfil del solista
                elif session['tipo'] == 3:  # Si el tipo de usuario es 3 (ambos)
                    if session['name'] == 'admin' and session['email'] == 'admin@admin.com':  # Si el usuario es el administrador
                        return render_template("perfiles/admin.html")  # Renderiza la plantilla para el perfil del administrador
                    else:
                        return render_template("perfiles/ambos/homeThree.html")  # Renderiza la plantilla para el perfil de ambos
                else:
                    notificacion.title = "Error de Acceso"
                    notificacion.message = "Tipo de usuario no válido"
                    notificacion.send()  # Envía una notificación de error
                    return render_template("login.html")  # Renderiza la plantilla de inicio de sesión nuevamente
            else:
                notificacion.title = "Error de Acceso"
                notificacion.message = "Correo o contraseña no válida"
                notificacion.send()  # Envía una notificación de error
                return render_template("login.html")  # Renderiza la plantilla de inicio de sesión nuevamente
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message = "No existe el usuario"
            notificacion.send()  # Envía una notificación de error
            return render_template("login.html")  # Renderiza la plantilla de inicio de sesión nuevamente
    else:  # Si la solicitud es de tipo GET (se accede directamente a la página de inicio de sesión)
        if 'email' in session:  # Si existe la variable de sesión 'email'
            tipo = session['tipo']  # Obtiene el tipo de usuario de la variable de sesión
            if tipo == 1:  # Si el tipo de usuario es 1 (banda)
                return render_template("perfiles/banda/home.html")  # Renderiza la plantilla para el perfil de la banda
            elif tipo == 2:  # Si el tipo de usuario es 2 (solista)
                return render_template("perfiles/solista/homeTwo.html")  # Renderiza la plantilla para el perfil del solista
            elif tipo == 3:  # Si el tipo de usuario es 3 (ambos)
                if session['name'] == "admin":  # Si el usuario es el administrador
                    return render_template("perfiles/admin.html")  # Renderiza la plantilla para el perfil del administrador
                else:
                    return render_template("perfiles/ambos/homeThree.html")  # Renderiza la plantilla para el perfil de ambos
                
        return render_template("login.html")  # Renderiza la plantilla de inicio de sesión



@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/registro', methods=["GET", "POST"])
def registro():
    # Consulta a la base de datos para obtener los tipos de usuario disponibles
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tip_usu")
    tipo = cur.fetchall()
    cur.close()

    notificacion = Notify()

    if request.method == 'GET':
        # Si la solicitud es GET, renderiza el formulario de registro con los tipos de usuario
        return render_template("registro.html", tipo=tipo)

    else:
        # Si la solicitud es POST, se reciben los datos del formulario de registro
        name = request.form['name']
        email = request.form['email']

        # Verificar si el nombre o correo electrónico ya existen en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE name = %s OR email = %s", (name, email))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            # Si el nombre o correo electrónico ya existen, se muestra una notificación y se redirige al formulario de registro nuevamente
            notificacion.title = "Registro Fallido"
            notificacion.message = "El nombre o correo electrónico ya está en uso"
            notificacion.send()
            return redirect(url_for('registro'))

        password = request.form['password']
        tip = request.form['tipo']
        descripcion = request.form['descripcion']

        # Insertar los datos del nuevo usuario en la base de datos
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usuarios (name, email, password, id_tip_usu, descripcion) VALUES (%s,%s,%s,%s,%s)",
            (name, email, password, tip, descripcion))
        mysql.connection.commit()

        # Mostrar una notificación de registro exitoso y redirigir al usuario a la página de inicio de sesión
        notificacion.title = "Registro Exitoso"
        notificacion.message = "Ya te encuentras registrado en Harmony, por favor inicia sesión y empieza a dar a conocer tu música"
        notificacion.send()
        return redirect(url_for('login'))

    
#############################################################################################################
#############################################################################################################

################################### P E R F I L E S ###########################################################


@app.route('/perfil')
def perfil():
    if 'email' not in session:
        return redirect(url_for('login'))
    
# Obtener información del usuario de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = %s", (session['email'],))
    usuario = cur.fetchone()
    cur.close()
# Obtener el tipo de usuario
    tipo = session['tipo']


# Renderizar la plantilla correspondiente según el tipo de usuari
    if tipo == 1:
        return render_template("/perfiles/banda/home.html", usuario=usuario)
    elif tipo == 2:
        return render_template("/perfiles/solista/homeTwo.html", usuario=usuario)
    elif tipo == 3:
         # Verificar si el usuario es el administrador
        if session['name'] == 'admin' and session['email'] == 'admin@admin.com':
            return render_template("/perfiles/admin.html")
        else:
            return render_template("/perfiles/ambos/homeThree.html", usuario=usuario)


@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    cur = mysql.connection.cursor()
    
    notificacion = Notify()

    if request.method == 'POST':
        # Obtener los datos del formulario de edición de perfil
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        id_tip_usu = request.form['id_tip_usu']
        descripcion = request.form['descripcion']

        
      # Actualizar los datos del usuario en la base de datos
        cur.execute("UPDATE usuarios SET name = %s, email = %s, password = %s, id_tip_usu = %s, descripcion = %s WHERE id = %s",
                    (name, email, password, id_tip_usu, descripcion, session['id']))
        mysql.connection.commit()

       # Obtener los datos actualizados del usuario
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (session['id'],))
        usuario = cur.fetchone()

        cur.close()
    # Actualizar los datos en la sesión
        session['name'] = usuario['name'] 
        session['email'] = usuario['email']
        session['password'] = usuario['password']
        session['id_tip_usu'] = usuario['id_tip_usu']
        session['descripcion'] = usuario['descripcion']
         # Enviar una notificación de éxito
        notificacion.title = "Edición exitosa"
        notificacion.message = "'¡Tu perfil se ha actualizado!"
        notificacion.send()

        return redirect(url_for('perfil'))

    else:
        # Obtener los datos del usuario actual para prellenar el formulario de edición
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (session['id'],))
        usuario = cur.fetchone()
        cur.close()

        return render_template('editar_perfil.html', usuario=usuario)


@app.route('/perfiles', methods=['GET', 'POST'])
def perfiles():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Si el método de solicitud es POST, se obtiene el nombre del usuario ingresado en el formulario de búsqueda
        name = request.form['name']

        # Ejecutar la consulta para obtener los perfiles de usuario por nombre
        cur.execute("SELECT name,email,nom_tip_usu,descripcion FROM usuarios NATURAL JOIN tip_usu WHERE name LIKE %s", ('%' + name + '%',))
        usuarios = cur.fetchall()

    else:
        # Si el método de solicitud es GET, no se proporciona un nombre en el formulario de búsqueda, por lo que se obtienen todos los perfiles de usuario
        # Ejecutar la consulta para obtener todos los perfiles de usuario
        cur.execute("SELECT name,email,nom_tip_usu,descripcion FROM usuarios NATURAL JOIN tip_usu")
        usuarios = cur.fetchall()
     

    cur.close()
    return render_template('perfiles/perfiles.html', usuarios=usuarios)


        
#########################################################################################################
#########################################################################################################
    
############################################### B L O G ######################################################
@app.route('/blogs')
def ver_blogs():
    # Obtener los parámetros de paginación
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

    # Crear la instancia de paginación
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('blog/blogs.html', blogs=blogs, pagination=pagination)


@app.route('/escribe_blog', methods=['GET', 'POST'])
def escribir_blog():
    
    # Verificar si el usuario ha iniciado sesión
    if 'email' not in session:
        return redirect(url_for('login'))

    # Obtener el ID del usuario de la sesión actual
    id_usuario = session.get('id')

    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el método POST
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        id_usuario = session['id']

        cur = mysql.connection.cursor()
        notificacion = Notify()
        
        # Insertar el nuevo blog en la base de datos
        cur.execute("INSERT INTO blogs (titulo, contenido, fecha, id) VALUES (%s, %s, NOW(), %s)", (titulo, contenido, id_usuario))
        mysql.connection.commit()

        cur.close()

        # Configurar notificación de éxito
        notificacion.title = "Publicado con éxito"
        notificacion.message = "Has publicado en Harmony"
        notificacion.send()

        # Redirigir al usuario a la página de ver blogs
        return redirect(url_for('ver_blogs'))
        
    else:
        # Mostrar el formulario de creación de blogs
        return render_template('blog/create.html', id=id_usuario)



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
    notificacion = Notify() 

    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el método POST
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        fecha = datetime.datetime.now()
# Actualizar el blog en la base de datos
        cur.execute("UPDATE blogs SET titulo = %s, contenido = %s, fecha = %s WHERE id_blog = %s",
                    (titulo, contenido, fecha, id_blog))
        mysql.connection.commit()

        flash('El blog ha sido actualizado exitosamente', 'success')
 # Obtener el blog actualizado desde la base de datos
        cur.execute("SELECT * FROM blogs WHERE id_blog = %s", (id_blog,))
        blog = cur.fetchone()

        cur.close()

        # Redirigir al usuario a la página de ver blogs
        notificacion.title = "Has editado tu publicación"
        notificacion.message = "Tu publicación ha sido actualizada"
        notificacion.send()
        return redirect(url_for('ver_blogs'))

    else:
        cur.execute("SELECT * FROM blogs WHERE id_blog = %s", (id_blog,))
        blog = cur.fetchone()
        cur.close()

        return render_template('blog/editar_blog.html', blog=blog)
    

################################################################################################
################################################################################################    

######################## B O R R A R , E D I T A R  U S U A R I O S ############################

@app.route('/adminPerfiles')
def adminPerfiles():
    # Verificar si el usuario ha iniciado sesión y es un administrador ('name' está en la sesión y es igual a 'admin')
    if 'name' in session and session['name'] == 'admin':
        cur = mysql.connection.cursor()

        # Obtener la lista de usuarios desde la base de datos
        cur.execute("SELECT id, name, email, password, id_tip_usu, descripcion FROM usuarios")
        usuarios = cur.fetchall()

        cur.close()

        # Renderizar la plantilla borrar_usuario.html y pasar la lista de usuarios como contexto
        return render_template('borrar_usuario.html', usuarios=usuarios)

    return 'Acceso no autorizado'

@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    notificacion = Notify()  
    # Verificar si el usuario ha iniciado sesión y es un administrador ('name' está en la sesión y es igual a 'admin')
    if 'name' in session and session['name'] == 'admin':
        cur = mysql.connection.cursor()

        # Eliminar el usuario de la base de datos utilizando su ID
        cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        mysql.connection.commit()

        cur.close()

    # Redireccionar a la página de administración de perfiles
    notificacion.title = "Eliminacion de usuario"
    notificacion.message = "'¡Has eliminado correctamente al usuario!"
    notificacion.send()
    return redirect(url_for('adminPerfiles'))

@app.route('/actualizar_usuario/<int:id>', methods=['GET', 'POST'])
def actualizar_usuario(id):
    notificacion = Notify()  # Creación de una instancia de la clase Notify para enviar notificaciones

    cur = mysql.connection.cursor()
    

    if request.method == 'POST':
        # Verificar si el método de solicitud es POST, lo que indica que se ha enviado el formulario de actualización de usuario y se deben procesar los datos.

        # Obtener los datos del formulario enviado a través del método POST
        name = request.form['name']
        email = request.form['email']
        id_tip_usu = request.form['id_tip_usu']
        password = request.form['password']
        descripcion = request.form['descripcion']

        # Actualizar los datos del usuario en la base de datos utilizando su ID
        cur.execute("UPDATE usuarios SET name = %s, email = %s, id_tip_usu = %s , password = %s, descripcion = %s WHERE id = %s",
                    (name, email, id_tip_usu, password, descripcion, id))
        mysql.connection.commit()

        # Obtener los datos actualizados del usuario desde la base de datos
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cur.fetchone()

        cur.close()
        notificacion.title = "Actualización de usuario"
        notificacion.message = "'¡Has actualizado correctamente el perfil!"
        notificacion.send()

        # Redireccionar a la página de perfiles
        return redirect(url_for('perfiles'))

    else:
        # Obtener los datos del usuario a actualizar desde la base de datos utilizando su ID
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cur.fetchone()
        cur.close()

        # Renderizar la plantilla actualizar_usuario.html y pasar los datos del usuario como contexto
        return render_template('actualizar_usuario.html', usuario=usuario)

    
##############################################################



if __name__ == '__main__':
    app.secret_key = "clavedepatricia"
    app.run(debug=True)

