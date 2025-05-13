import re
from flask import Flask, request, render_template, jsonify, session, redirect
import pandas as pd

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Necesaria para usar sesiones

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del formulario HTML
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    
    # Lee el archivo XLSX con openpyxl
    df = pd.read_excel("base de datos.xlsx", engine="openpyxl")
    
    # Revisa si hay alguna fila que coincida con usuario y contraseña
    usuario_valido = df[(df['usuario'] == usuario) & (df['contrasena'] == contrasena)]

    # Validar credenciales
    if not usuario_valido.empty:
        session['usuario'] = usuario
        session['contrasena'] = contrasena
        return render_template("consulta.html", user=session['usuario'], password=session['contrasena'])
    else:
        return "❌ Usuario o contraseña incorrectos"

@app.route('/consulta')
def bienvenido():
    if 'usuario' in session:
        return render_template("consulta.html", user=session['usuario'], password=session['contrasena'])
    else:
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
