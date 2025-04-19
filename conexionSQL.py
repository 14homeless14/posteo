from flask import Flask, render_template, request, redirect, session 
import mysql.connector

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Clave secreta necesaria para usar sesiones (mantener datos entre solicitudes)
app.secret_key = 'clave-super-secreta'  # 🔒 Cámbiala por algo más seguro en producción

# ----------------------------------------------
# FUNCIÓN: verificar_usuario
# Descripción: Verifica si las credenciales del usuario existen en la base de datos
# Parámetros: 
#   - usuario: nombre de usuario ingresado
#   - clave: contraseña ingresada
# Retorna:
#   - True si el usuario existe y la contraseña coincide
#   - False si no hay coincidencia
# ----------------------------------------------
def verificar_usuario(usuario, clave):
    # Establecer conexión con la base de datos MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  # 🔑 Cambia por tu contraseña real
        database="registroReportes"  # 📁 Asegúrate de que esta base de datos exista
    )
    cursor = conn.cursor()

    # Ejecutar consulta para verificar credenciales
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND clave = %s", (usuario, clave))
    resultado = cursor.fetchone()  # Obtiene el primer resultado (si existe)

    # Cerrar la conexión
    conn.close()

    return resultado is not None  # Devuelve True si encontró al usuario

# ----------------------------------------------
# RUTA: /
# Descripción: Muestra el formulario de login
# Método: GET
# ----------------------------------------------
@app.route('/')
def index():
    return render_template('login.html')

# ----------------------------------------------
# RUTA: /login
# Descripción: Procesa el formulario de login
# Método: POST
# ----------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del formulario HTML
    usuario = request.form['userSGA']
    clave = request.form['passwordSGA']

    # Validar credenciales
    if verificar_usuario(usuario, clave):
        # Guardar el usuario en la sesión
        session['usuario'] = usuario
        return redirect('/consulta')  # Redirige a la página protegida
    else:
        return "❌ Usuario o contraseña incorrectos"  # Mostrar mensaje si falló

# ----------------------------------------------
# RUTA: /consulta
# Descripción: Página protegida, solo accesible si hay sesión iniciada
# Método: GET
# ----------------------------------------------
@app.route('/consulta')
def bienvenido():
    # Verificar si el usuario está en la sesión
    if 'usuario' in session:
        # Renderiza la página y pasa el nombre de usuario
        return render_template("consulta.html", usuario=session['usuario'])
    else:
        # Si no hay sesión activa, redirige al login
        return redirect('/')

# ----------------------------------------------
# RUTA: /logout
# Descripción: Cierra la sesión del usuario
# Método: GET
# ----------------------------------------------
@app.route('/logout')
def logout():
    # Elimina al usuario de la sesión
    session.pop('usuario', None)
    return redirect('/')  # Redirige al login

# ----------------------------------------------
# EJECUCIÓN DEL SERVIDOR
# Descripción: Inicia el servidor Flask en modo debug
# ----------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
