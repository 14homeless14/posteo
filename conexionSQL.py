from flask import Flask, render_template, request, redirect
import mysql.connector

# Crear la aplicación Flask
app = Flask(__name__)

# Función para verificar las credenciales del usuario en la base de datos
def verificar_usuario(usuario, clave):
    # Conexión a la base de datos MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  # 🔒 Cambia esto por tu contraseña real
        database="registroReportes"  # Asegúrate de que esta base de datos exista
    )
    cursor = conn.cursor()

    # Consulta para verificar si el usuario existe con esa clave
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND clave = %s", (usuario, clave))

    resultado = cursor.fetchone()  # Devuelve la primera coincidencia (o None si no hay)
    conn.close()

    return resultado is not None  # Devuelve True si encontró al usuario

# Ruta raíz (muestra el formulario de login)
@app.route('/')
def index():
    return render_template('login.html')  # El archivo debe estar en /templates

# Ruta que procesa los datos del formulario
@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['userSGA']  # Obtiene el valor del input con name="usuario"
    clave = request.form['passwordSGA']      # Obtiene la clave

    # Verifica si el usuario es válido
    if verificar_usuario(usuario, clave):
        return redirect('/bienvenido')  # Redirige a otra página si es correcto
    else:
        return "❌ Usuario o contraseña incorrectos"

# Página mostrada si el login es exitoso
@app.route('/bienvenido')
def bienvenido():
    return "¡Inicio de sesión exitoso!"  # Puedes reemplazar esto por un render_template

# Inicia el servidor web en modo debug
if __name__ == '__main__':
    app.run(debug=True)
