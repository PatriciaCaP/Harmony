from flask import Flask,  render_template, request, redirect, url_for, session # pip install Flask
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from os import path #pip install notify-py
from notifypy import Notify
import random

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'btug0fx7ljzszoqysnwl-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'up8pf5catvcodukz'
app.config['MYSQL_PASSWORD'] = 'wEo63IA2urQveLCLPiWl'
app.config['MYSQL_DB'] = 'btug0fx7ljzszoqysnwl'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

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
        "La música es el único amor verdadero. - Jack White"
    
    ]
    frase_aleatoria = random.choice(frases)
    return render_template('principal.html', frase=frase_aleatoria)

@app.route('/blog', methods=['GET', 'POST'])
def escribir_blog():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        id = request.form['id']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blogs (titulo, contenido, fecha, id) VALUES (%s, %s, NOW(), %s)",(titulo, contenido, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home'))
    else:
        return render_template('blog.html')

@app.route('/blogs')
def ver_blogs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT blogs.*, usuarios.name AS nombre_autor FROM blogs INNER JOIN usuarios ON blogs.id = usuarios.id")
    blogs = cur.fetchall()
    cur.close()

    return render_template('blog.html', blogs=blogs)
 

@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("contenido.html")


@app.route('/login', methods= ["GET", "POST"])
def login():

    notificacion = Notify()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user)>0:
            if password == user["password"]:
                session['name'] = user['name']
                session['email'] = user['email']
                session['tipo'] = user['id_tip_usu']

                if session['tipo'] == 1:
                    return render_template("banda/home.html")
                elif session['tipo'] == 2:
                    return render_template("solista/homeTwo.html")
                elif session['tipo'] == 3:
                    return render_template("ambos/homeThree.html")


            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Correo o contraseña no valida"
                notificacion.send()
                return render_template("login.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="No existe el usuario"
            notificacion.send()
            return render_template("login.html")
    else:
        
        return render_template("login.html")



@app.route('/registro', methods = ["GET", "POST"])
def registro():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tip_usu")
    tipo = cur.fetchall()
    cur.close()

    notificacion = Notify()
    
    

    if request.method == 'GET':
        return render_template("registro.html", tipo = tipo )
    
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        tip = request.form['tipo']
    

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (name, email, password, id_tip_usu) VALUES (%s,%s,%s,%s)", (name, email, password,tip))
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="Ya te encuentras registrado en Harmony, por favor inicia sesión y empieza a dar a conocer tu música"
        notificacion.send()
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = "clavedepatricia"
    app.run(debug=True)