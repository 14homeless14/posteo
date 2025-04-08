from flask import Flask, request, redirect, session, render_template
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura"

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="tu_usuario",
    password="tu_contraseña",
    database="mi_base_de_datos"
)

@app.route('/', methods=['GET'])
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    cursor = db.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE nombre_usuario = %s", (usuario,))
    resultado = cursor.fetchone()

    if resultado and bcrypt.checkpw(contrasena.encode('utf-8'), resultado[0].encode('utf-8')):
        session['usuario'] = usuario  # Iniciar sesión
        return redirect('/posteo')
    else:
        return "Usuario o contraseña incorrectos", 401

@app.route('/posteo')
def posteo():
    if 'usuario' not in session:
        return redirect('/')
    return f"Bienvenido, {session['usuario']}"

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')