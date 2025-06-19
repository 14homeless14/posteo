#pip install flask mysql-connector-python
import re
from flask import Flask, request, render_template, jsonify, session, redirect, url_for, flash

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dateutil import parser
import time
import pandas as pd
from datetime import datetime
from werkzeug.security import check_password_hash  # si usas contraseñas encriptadas

app = Flask(__name__)
app.secret_key = 'pito'  # Necesaria para usar sesiones

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del formulario HTML
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    
    # Lee el archivo XLSX con openpyxl
    df = pd.read_excel("base de datos.xlsx", sheet_name="usuarios", engine="openpyxl")
    # Verifica que los datos del formulario se reciban correctamente

    # Revisa si hay alguna fila que coincida con usuario y contraseña
    usuario_valido = df[(df['usuario'] == usuario) & (df['contrasena'] == contrasena)]

    # Validar credenciales
    if not usuario_valido.empty:
        session['usuario'] = usuario
        session['contrasena'] = contrasena
        return render_template("consulta.html", user=session['usuario'], password=session['contrasena'])
    else:
        return render_template('login.html', error='Usuario o contraseña incorrecta')

        

@app.route('/consulta')
def bienvenido():
    if 'usuario' in session:
        return render_template("consulta.html", user=session['usuario'], password=session['contrasena'])
    else:
       return render_template('login.html', error='Usuario o contraseña incorrecta')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    return render_template('login.html')

datos = {}  # Variable global para almacenar los datos obtenidos
@app.route("/scrape", methods=["POST"])
def scrape():
    # Lee el archivo XLSX con openpyxl
    df = pd.read_excel("base de datos.xlsx", sheet_name="usuarios", engine="openpyxl")
    # Verifica que el usuario esté en sesión

    # Verifica que los datos del formulario se reciban correctamente
    usuario = session.get("usuario")# Obtén el usuario de la sesión #"elorenzo"
    contrasena = session.get("contrasena")#"pinolillo123"
    numeroTT = request.form.get("numeroTT")
    fila = df[df["usuario"] == usuario]
    nombre = fila["nombre del usuario"].iloc[0]

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

        tiempoTrascurriodeTT = (f"Diferencia: {diferencia_dias} dias, {horas_diferencia} horas, "
                                f"{minutos_diferencia} minutos, {segundos_diferencia} segundos")

    # Cálculo de diferencia entre fechaAlarm y la fecha más reciente de SGA
    if fecha_detectadaOT and fecha_detectadaTT:
        diferencia2 = fecha_detectadaOT - fecha_detectadaTT
        diferencia_segundos = int(diferencia2.total_seconds())

        diferencia_dias2 = diferencia_segundos // (24 * 60 * 60)
        horas_diferencia2 = (diferencia_segundos % (24 * 60 * 60)) // (60 * 60)
        minutos_diferencia2 = (diferencia_segundos % (60 * 60)) // 60
        segundos_diferencia2 = diferencia_segundos % 60

        tiempoTrascurriodeTTyOT = (f"Diferencia: {diferencia_dias2} dias, {horas_diferencia2} horas, "
                                   f"{minutos_diferencia2} minutos, {segundos_diferencia2} segundos")

    # Procesar los datos obtenidos
    informacion = {
        "nombre": nombre,
        "numeroTT": ticketId,
        "fechaAlarm": fechaAlarm,
        "descripcion": descripcion,
        "tituloFalla": titulo,
        "nodo": nodo,
        "sucursal": sistema,
        "numSucursal": numSucursal,
        "sga": sga,
        "fechaDetectadaOTEnSGA": str(fecha_detectadaOT) if fecha_detectadaOT else "No se detectó una fecha",
        "tiempoDeTT": tiempoTrascurriodeTT,
        "tiempoDeTTyOT": tiempoTrascurriodeTTyOT,
    }
    return render_template("posteo.html",datos=informacion)#Retornar los datos como JSON jsonify(informacion)#


@app.route('/posteo', methods=['POST'])
@app.route('/posteo', methods=['GET', 'POST'])
def guardar_posteo():
    if request.method == 'POST':
        datos_formulario = {
            'Nombre': request.form.get('tuNombre'),
            'Tipo de Falla': request.form.get('tipoFalla'),
            'Folio OT': request.form.get('folioOT'),
            'Clientes Afectados': request.form.get('clientesAfectados'),
            'Coordenadas': request.form.get('coordenadas'),
            'CTC o Hub': request.form.get('ctcHub'),
            'Alarma': request.form.get('alarma'),
            'Datos Adicionales': request.form.get('datosAdicionales'),
            'Validación': request.form.get('status'),
            'Tiempo TT': request.form.get('tiempoDeTT'),
            'Número Sucursal': request.form.get('numSucursal'),
            'Sucursal': request.form.get('sucursal'),
            'Título Falla': request.form.get('tituloFalla'),
            'Ticket TT': request.form.get('numeroTT'),
            'Nodo o Puerto': request.form.get('nodo'),
            'Fecha OT': request.form.get('fechaDetectadaOTEnSGA'),
            'Fecha Alarm': request.form.get('fechaAlarm'),
            'Datos SGA': request.form.get('sga'),
            'Descripción': request.form.get('descripcion'),
        }

        try:
            # Leer ambas hojas
            xls = pd.read_excel('base de datos.xlsx', sheet_name=None, engine='openpyxl')

            # Obtener el orden correcto desde la hoja "registros"
            registros_existentes = xls.get("registros", pd.DataFrame())
            columnas = registros_existentes.columns.tolist() if not registros_existentes.empty else list(datos_formulario.keys())

            nuevo_registro = pd.DataFrame([datos_formulario])[columnas]

            # Concatenar el nuevo registro
            df_actualizado = pd.concat([registros_existentes, nuevo_registro], ignore_index=True)

            # Escribir de nuevo las dos hojas
            with pd.ExcelWriter('base de datos.xlsx', engine='openpyxl', mode='w') as writer:
                xls['usuarios'].to_excel(writer, sheet_name='usuarios', index=False)
                df_actualizado.to_excel(writer, sheet_name='registros', index=False)

        except FileNotFoundError:
            # Si no existe, crea ambas hojas desde cero
            with pd.ExcelWriter('base de datos.xlsx', engine='openpyxl') as writer:
                pd.DataFrame(columns=['usuario', 'contrasena', 'nombre del usuario']).to_excel(writer, sheet_name='usuarios', index=False)
                pd.DataFrame([datos_formulario]).to_excel(writer, sheet_name='registros', index=False)

        flash("✅ Registro guardado exitosamente")
        return redirect(url_for('bienvenido'))



if __name__ == '__main__':
    app.run(debug=True)
