#pip install flask mysql-connector-python

import re
from flask import Flask, request, render_template, redirect, url_for,jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dateutil import parser
import time
from datetime import datetime
from werkzeug.security import check_password_hash  # si usas contraseñas encriptadas
import mysql.connector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("iniciarSesion.html")  # Página de inicio de sesión  

@app.route("/scrape", methods=["POST"])
def scrape():
    # Verifica que los datos del formulario se reciban correctamente
    usuario = request.form.get("usuario")
    contrasena = request.form.get("contrasena")
    numeroTT = request.form.get("numeroTT")

    if not usuario or not contrasena or not numeroTT:
        return jsonify({"error": "Faltan datos en el formulario"}), 400
    
    # Configuración del navegador
    options = Options()
    driver = webdriver.Chrome(options=options)
    
    # Navegar a la página de login
    driver.get("http://sgn.iyarnoc/login")
    time.sleep(2)
    
    # Iniciar sesión
    campo_usuario = driver.find_element(By.NAME, "usuario")
    campo_usuario.send_keys(usuario)
    
    campo_contrasena = driver.find_element(By.NAME, "password")
    campo_contrasena.send_keys(contrasena)
    campo_contrasena.send_keys(Keys.RETURN)
    time.sleep(2)
    
    # Navegar a la página siguiente
    driver.get("http://sgn.iyarnoc/ordenesOTConEquipo2")
    time.sleep(2)
    
    # Buscar el campo de número de ticket
    campo_texto = driver.find_element(By.ID, 'ticketId')
    campo_texto.send_keys(numeroTT)
    campo_texto.send_keys(Keys.RETURN)
    time.sleep(7)
    
    # Obtener los valores de cada campo
    ticketId = driver.execute_script('return document.getElementById("ticketId").value')
    fechaAlarm = driver.execute_script('return document.formOT.fechaAlarm.value')
    descripcion = driver.execute_script('return document.formOT.descripcion.value')
    titulo = driver.execute_script('return document.formOT.titulo.value')
    nodo = driver.execute_script('return document.formOT.nodo.value')
    sistema = driver.execute_script('return document.formOT.sistema.value')
    numSucursal = driver.execute_script('return document.formOT.numSucursal.value')
    sga = driver.execute_script('return document.formOT.sga.value')
    
    driver.quit()

    # Detección de múltiples fechas en el texto de "sga"
    def detectar_fechas(sga):
        #Busca y extrae todas las fechas en formato YYYY-MM-DD HH:MM:SS dentro del texto de sga.
        #Retorna una lista de objetos datetime con las fechas encontradas.
        
        patron_fecha = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        coincidencias = re.findall(patron_fecha, sga)
        
        fechas = []
        for fecha_str in coincidencias:
            try:
                fecha = parser.parse(fecha_str)
                fechas.append(fecha)
            except ValueError:
                continue  # Si no se puede analizar, se ignora
        
        return fechas  # Retorna una lista de fechas encontradas

    def detectar_fechaTT(fechaAlarm):
        #Convierte una fecha en texto en un objeto datetime.
        #Si la conversión falla, retorna None.
        
        try:
            return parser.parse(fechaAlarm)
        except ValueError:
            return None

    # Usamos la función para detectar fechas en "sga"
    fechas_detectadasOT = detectar_fechas(sga)
    fecha_detectadaTT = detectar_fechaTT(fechaAlarm)

    # Si se detectan fechas en "sga", tomamos la más reciente
    fecha_detectadaOT = max(fechas_detectadasOT) if fechas_detectadasOT else None

    tiempoTrascurriodeTT = "No se detectó una fecha en TT"
    tiempoTrascurriodeTTyOT = "No se detectó una fecha en OT"

    # Cálculo de diferencia de tiempo con fechaAlarm
    if fecha_detectadaTT:
        fecha_actual = datetime.now()
        diferencia = fecha_actual - fecha_detectadaTT
        diferencia_segundos = int(diferencia.total_seconds())

        diferencia_dias = diferencia_segundos // (24 * 60 * 60)
        horas_diferencia = (diferencia_segundos % (24 * 60 * 60)) // (60 * 60)
        minutos_diferencia = (diferencia_segundos % (60 * 60)) // 60
        segundos_diferencia = diferencia_segundos % 60

        tiempoTrascurriodeTT = (f"Diferencia: {diferencia_dias} días, {horas_diferencia} horas, "
                                f"{minutos_diferencia} minutos, {segundos_diferencia} segundos")

    # Cálculo de diferencia entre fechaAlarm y la fecha más reciente de SGA
    if fecha_detectadaOT and fecha_detectadaTT:
        diferencia2 = fecha_detectadaOT - fecha_detectadaTT
        diferencia_segundos = int(diferencia2.total_seconds())

        diferencia_dias2 = diferencia_segundos // (24 * 60 * 60)
        horas_diferencia2 = (diferencia_segundos % (24 * 60 * 60)) // (60 * 60)
        minutos_diferencia2 = (diferencia_segundos % (60 * 60)) // 60
        segundos_diferencia2 = diferencia_segundos % 60

        tiempoTrascurriodeTTyOT = (f"Diferencia: {diferencia_dias2} días, {horas_diferencia2} horas, "
                                   f"{minutos_diferencia2} minutos, {segundos_diferencia2} segundos")

    # Procesar los datos obtenidos
    data = {
        "ticketId": ticketId,
        "fechaAlarm": fechaAlarm,
        "descripcion": descripcion,
        "titulo": titulo,
        "nodo": nodo,
        "sistema": sistema,
        "numSucursal": numSucursal,
        "sga": sga,
        "fechaDetectadaOT": str(fecha_detectadaOT) if fecha_detectadaOT else "No se detectó una fecha",
        "tiempoDeTT": tiempoTrascurriodeTT,
        "tiempoDeTTyOT": tiempoTrascurriodeTTyOT,
    }
    return jsonify(data)  # Retornar los datos como JSON

@app.route("/posteo")
def posteo():
    return render_template("posteo.html")  # Página de posteo

if __name__ == "__main__":
    app.run(debug=True)