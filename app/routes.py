from app import app  # Importamos la instancia 'app' desde __init__.py
from flask import request, render_template, redirect, url_for, flash
import os
import pandas as pd
from app.models import get_db_connection
from app.data_cleaning import limpiar_datos as limpiar_datos_script

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/limpiar_datos', methods=['POST'])
def limpiar_datos():
    total_antes, total_despues = limpiar_datos_script()
    flash(f"Datos limpiados correctamente. Filas antes: {total_antes}, después: {total_despues}.", "success")
    return redirect(url_for('listar_clientes'))

@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    cliente_id = request.form['cliente_id']

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clientes WHERE cliente_id = %s", (cliente_id,))
        connection.commit()
        connection.close()
        flash("Cliente eliminado correctamente", "success")
    except Exception as e:
        flash(f"Error al eliminar el cliente: {e}", "danger")

    return redirect(url_for('listar_clientes'))

@app.route('/eliminar_todos_clientes', methods=['POST'])
def eliminar_todos_clientes():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clientes")
        connection.commit()
        connection.close()
        flash("Todos los clientes han sido eliminados", "warning")
    except Exception as e:
        flash(f"Error al eliminar todos los clientes: {e}", "danger")

    return redirect(url_for('listar_clientes'))

@app.route('/ingresar_cliente', methods=['POST'])
def ingresar_cliente():
    nombre = request.form['nombre']
    edad = request.form['edad']
    genero = request.form['genero']
    ingreso_mensual = request.form['ingreso_mensual']
    saldo_cuenta = request.form['saldo_cuenta']
    productos_contratados = request.form['productos_contratados']
    historial_credito = request.form['historial_credito']
    cantidad_prestamos = request.form['cantidad_prestamos']
    monto_total_prestamos = request.form['monto_total_prestamos']
    estado_civil = request.form['estado_civil']
    ocupacion = request.form['ocupacion']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO clientes (nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, 
        cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, 
          cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion))
    connection.commit()
    connection.close()

    flash("Cliente ingresado exitosamente", "success")
    return redirect(url_for('home'))

@app.route('/listar_clientes')
def listar_clientes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    connection.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No se subió ningún archivo", "error")
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        flash("El archivo no tiene nombre", "error")
        return redirect(url_for('home'))

    try:
        df = pd.read_csv(file)

        connection = get_db_connection()
        cursor = connection.cursor()

        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO clientes (nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, 
                cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['nombre'], row['edad'], row['genero'], row['ingreso_mensual'], row['saldo_cuenta'], 
                  row['productos_contratados'], row['historial_credito'], row['cantidad_prestamos'], 
                  row['monto_total_prestamos'], row['estado_civil'], row['ocupacion']))
        
        connection.commit()
        connection.close()

        flash("Archivo CSV procesado correctamente", "success")
    except Exception as e:
        flash(f"Error al procesar el archivo: {e}", "error")

    return redirect(url_for('home'))

@app.route('/analisis')
def analisis():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            COUNT(*) AS total_clientes,
            SUM(saldo_cuenta) AS saldo_total,
            AVG(edad) AS promedio_edad,
            AVG(ingreso_mensual) AS promedio_ingreso,
            COUNT(*) AS total_prestamos,
            SUM(monto_total_prestamos) AS monto_total_prestamos,
            AVG(historial_credito) AS promedio_historial_credito
        FROM clientes
    """)
    resumen = cursor.fetchone()
    connection.close()
    return render_template('analisis.html', resumen=resumen)
