from app import app  # Importamos la instancia 'app' desde __init__.py
from flask import request, render_template, redirect, url_for, flash
import os
import pandas as pd
from app.models import get_db_connection


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No se subió ningún archivo", "error")
            return redirect(url_for('home'))
        file = request.files['file']
        if file.filename == '':
            flash("El archivo no tiene nombre", "error")
            return redirect(url_for('home'))

        # Guardar el archivo en la carpeta configurada
        file_path = os.path.join('data', file.filename)
        file.save(file_path)

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            flash(f"Error al leer el archivo: {e}", "error")
            return redirect(url_for('home'))

        # Mostrar resumen de datos
        resumen = {
            'rows': len(df),
            'columns': len(df.columns),
            'summary': df.describe().to_html()
        }
        return render_template('upload.html', resumen=resumen)

    return render_template('upload.html')


@app.route('/ingresar_cliente', methods=['POST'])
def ingresar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        genero = request.form['genero']
        ingreso_mensual = request.form['ingreso_mensual']
        saldo_cuenta = request.form['saldo_cuenta']
        productos_contratados = request.form['productos_contratados']

        # Conexión a la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insertar datos en la tabla clientes
        cursor.execute("""
            INSERT INTO clientes (nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados))

        connection.commit()
        connection.close()

        flash("Cliente ingresado exitosamente", "success")
        return redirect(url_for('home'))


@app.route('/ingresar_prestamo', methods=['POST'])
def ingresar_prestamo():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        monto_prestamo = request.form['monto_prestamo']
        tasa_interes = request.form['tasa_interes']
        plazo_prestamo = request.form['plazo_prestamo']
        historial_credito = request.form['historial_credito']
        pagos_atrasados = request.form['pagos_atrasados']
        es_default = request.form['es_default']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insertar datos en la tabla prestamos
        cursor.execute("""
            INSERT INTO prestamos (cliente_id, monto_prestamo, tasa_interes, plazo_prestamo, historial_credito, pagos_atrasados, es_default)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (cliente_id, monto_prestamo, tasa_interes, plazo_prestamo, historial_credito, pagos_atrasados, es_default))

        connection.commit()
        connection.close()

        flash("Préstamo ingresado exitosamente", "success")
        return redirect(url_for('home'))


@app.route('/ingresar_transaccion', methods=['POST'])
def ingresar_transaccion():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        fecha_transaccion = request.form['fecha_transaccion']
        tipo_transaccion = request.form['tipo_transaccion']
        monto = request.form['monto']
        ubicacion = request.form['ubicacion']
        fraude = request.form['fraude']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insertar datos en la tabla transacciones
        cursor.execute("""
            INSERT INTO transacciones (cliente_id, fecha_transaccion, tipo_transaccion, monto, ubicacion, fraude)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cliente_id, fecha_transaccion, tipo_transaccion, monto, ubicacion, fraude))

        connection.commit()
        connection.close()

        flash("Transacción ingresada exitosamente", "success")
        return redirect(url_for('home'))

@app.route('/clientes')
def listar_clientes():
    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Consultar todos los clientes
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    
    # Cerrar la conexión
    cursor.close()
    connection.close()
    
    # Renderizar el HTML con los datos
    return render_template('clientes.html', clientes=clientes)
