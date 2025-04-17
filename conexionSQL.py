from flask import Flask, request, redirect, session, render_template
import mysql.connector
import bcrypt

# Inicialización de la aplicación Flask
app = Flask(__name__)
# Clave secreta para manejar las sesiones de usuario
app.secret_key = "clave_secreta_super_segura"

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",       # Dirección del servidor de la base de datos
    user="tu_usuario",      # Usuario de la base de datos
    password="tu_contraseña",  # Contraseña del usuario
    database="mi_base_de_datos"  # Nombre de la base de datos
)

# Ruta para la página principal (GET)
@app.route('/', methods=['GET'])
def login_page():
    """
    Renderiza la página de inicio de sesión.
    """
    return render_template("login.html")

# Ruta para manejar el inicio de sesión (POST)
@app.route('/login', methods=['POST'])
def login():
    """
    Maneja el inicio de sesión del usuario.
    - Obtiene el nombre de usuario y la contraseña desde el formulario.
    - Verifica las credenciales contra la base de datos.
    - Si las credenciales son válidas, inicia sesión y redirige al área de posteo.
    - Si no son válidas, devuelve un error 401.
    """
    usuario = request.form['usuario']  # Nombre de usuario ingresado
    contrasena = request.form['contrasena']  # Contraseña ingresada

    # Consulta a la base de datos para obtener la contraseña del usuario
    cursor = db.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE nombre_usuario = %s", (usuario,))
    resultado = cursor.fetchone()

    # Verifica si la contraseña ingresada coincide con la almacenada (encriptada)
    if resultado and bcrypt.checkpw(contrasena.encode('utf-8'), resultado[0].encode('utf-8')):
        session['usuario'] = usuario  # Guarda el usuario en la sesión
        return redirect('/posteo')  # Redirige al área de posteo
    else:
        return "Usuario o contraseña incorrectos", 401  # Devuelve un error si las credenciales no son válidas

# Ruta para el área de posteo (GET)
@app.route('/posteo')
def posteo():
    """
    Muestra el área de posteo si el usuario ha iniciado sesión.
    - Si no hay un usuario en la sesión, redirige a la página de inicio de sesión.
    """
    if 'usuario' not in session:  # Verifica si el usuario está en la sesión
        return redirect('/')  # Redirige a la página de inicio de sesión
    return f"Bienvenido, {session['usuario']}"  # Muestra un mensaje de bienvenida

# Ruta para cerrar sesión (GET)
@app.route('/logout')
def logout():
    """
    Cierra la sesión del usuario.
    - Elimina al usuario de la sesión.
    - Redirige a la página de inicio de sesión.
    """
    session.pop('usuario', None)  # Elimina el usuario de la sesión
    return redirect('/')  # Redirige a la página de inicio de sesión