from app import app  # Importamos la instancia 'app' desde __init__.py
from flask import request, render_template, redirect, url_for, flash
import pandas as pd
from app.models import get_db_connection
from app.data_cleaning import limpiar_datos as limpiar_datos_script
from app.model_predict import predecir_cliente
from app.models import Clientes
from flask import render_template
from app.models import obtener_clientes, obtener_prestamos, obtener_transacciones, obtener_fraudes, obtener_pagos

def process_csv_file(file):
    df = pd.read_csv(file)
    df.fillna({
        'nombre': 'Desconocido',
        'edad': 0,
        'genero': 'No especificado',
        'ingreso_mensual': 0.00,
        'saldo_cuenta': 0.00,
        'productos_contratados': 0,
        'historial_credito': 1,
        'cantidad_prestamos': 0,
        'monto_total_prestamos': 0.00,
        'estado_civil': 'No especificado',
        'ocupacion': 'No especificado'
    }, inplace=True)
    df.replace({pd.NA: None, 'nan': None, 'NaN': None, '': None}, inplace=True)
    return df

@app.route('/upload_clientes', methods=['POST'])
def upload_clientes():
    if 'file' not in request.files:
        flash("No se subió ningún archivo", "error")
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        flash("El archivo no tiene nombre", "error")
        return redirect(url_for('home'))

    try:
        df = process_csv_file(file)

        connection = get_db_connection()
        cursor = connection.cursor()

        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO clientes (cliente_id, nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, 
                cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['cliente_id'], row['nombre'], row['edad'], row['genero'], row['ingreso_mensual'],
                row['saldo_cuenta'], row['productos_contratados'], row['historial_credito'],
                row['cantidad_prestamos'], row['monto_total_prestamos'], row['estado_civil'], row['ocupacion']
            ))

        connection.commit()
        connection.close()
        flash("Archivo CSV de clientes procesado correctamente", "success")
    except Exception as e:
        flash(f"Error al procesar el archivo CSV: {e}", "error")

    return redirect(url_for('home'))

@app.route('/prestamo')
def prestamo_home():
    return render_template('upload.html')

@app.route('/upload_prestamos', methods=['POST'])
def upload_prestamos():
    if 'file' not in request.files:
        flash("No se subió ningún archivo", "error")
        return redirect(url_for('prestamo_home'))
    
    file = request.files['file']
    if file.filename == '':
        flash("El archivo no tiene nombre", "error")
        return redirect(url_for('prestamo_home'))

    try:
        df = pd.read_csv(file)
        connection = get_db_connection()
        cursor = connection.cursor()

        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO prestamos (cliente_id, monto_prestamo, tasa_interes, plazo_meses, historial_credito, pagos_atrasados, estado_prestamo, fecha_inicio, fecha_vencimiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['cliente_id'], row['monto_prestamo'], row['tasa_interes'], row['plazo_meses'],
                  row['historial_credito'], row['pagos_atrasados'], row['estado_prestamo'], row['fecha_inicio'], row['fecha_vencimiento']))

        connection.commit()
        connection.close()

        flash("Archivo de préstamos procesado correctamente", "success")
    except Exception as e:
        flash(f"Error al procesar el archivo: {e}", "error")

    return redirect(url_for('prestamo_home'))

@app.route('/upload_fraudes', methods=['POST'])
def upload_fraudes():
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
                INSERT INTO fraudes (cliente_id, descripcion, monto_implicado, fecha_fraude, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['cliente_id'], row['descripcion'], row['monto_implicado'], row['fecha_fraude'], row['estado']))

        connection.commit()
        connection.close()

        flash("Archivo de fraudes procesado correctamente", "success")
    except Exception as e:
        flash(f"Error al procesar el archivo: {e}", "error")

    return redirect(url_for('home'))


@app.route('/upload_transacciones', methods=['POST'])
def upload_transacciones():
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
                INSERT INTO transacciones (cliente_id, tipo_transaccion, monto, fecha_transaccion, categoria_transaccion)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['cliente_id'], row['tipo_transaccion'], row['monto'], row['fecha_transaccion'], row['categoria_transaccion']))

        connection.commit()
        connection.close()

        flash("Archivo de transacciones procesado correctamente", "success")
    except Exception as e:
        flash(f"Error al procesar el archivo: {e}", "error")

    return redirect(url_for('home'))


@app.route('/upload_pagos', methods=['POST'])
def upload_pagos():
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
                INSERT INTO pagos (prestamo_id, monto_pagado, fecha_pago, metodo_pago)
                VALUES (%s, %s, %s, %s)
            """, (row['prestamo_id'], row['monto_pagado'], row['fecha_pago'], row['metodo_pago']))

        connection.commit()
        connection.close()

        flash("Archivo de pagos procesado correctamente", "success")
    except Exception as e:
        flash(f"Error al procesar el archivo: {e}", "error")

    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/predecir_cliente_view', methods=['POST'])
def predecir_cliente_view():
    cliente_id = request.form.get('cliente_id')
    nombre = request.form.get('nombre')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if cliente_id:
        cursor.execute("SELECT * FROM clientes WHERE cliente_id = %s", (cliente_id,))
    elif nombre:
        cursor.execute("SELECT * FROM clientes WHERE nombre = %s", (nombre,))
    else:
        flash("Debes ingresar un ID o un nombre para buscar.", "danger")
        return redirect(url_for('analisis'))

    cliente = cursor.fetchone()
    connection.close()

    if not cliente:
        flash("Cliente no encontrado.", "danger")
        return redirect(url_for('analisis'))

    from app.model_training import predecir_riesgo_cliente
    datos_cliente = [
        cliente['edad'], cliente['ingreso_mensual'], cliente['saldo_cuenta'],
        cliente['productos_contratados'], cliente['historial_credito'],
        cliente['cantidad_prestamos'], cliente['monto_total_prestamos']
    ]
    
    prediccion = predecir_riesgo_cliente(datos_cliente)

    return render_template('analisis.html', cliente=cliente, prediccion=prediccion)

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
    try:
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

    except KeyError as e:
        flash(f"Error al ingresar cliente: Falta el campo {e.args[0]}", "danger")
        return redirect(url_for('home'))

    except Exception as e:
        flash(f"Error al ingresar cliente: {str(e)}", "danger")
        return redirect(url_for('home'))

@app.route('/listar_clientes')
def listar_clientes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM clientes WHERE 1=1"
    filters = []

    nombre = request.args.get('nombre')
    edad = request.args.get('edad')
    genero = request.args.get('genero')
    ingreso_min = request.args.get('ingreso_min')
    ingreso_max = request.args.get('ingreso_max')
    saldo_min = request.args.get('saldo_min')
    saldo_max = request.args.get('saldo_max')

    if nombre:
        query += " AND nombre LIKE %s"
        filters.append(f"%{nombre}%")
    if edad:
        query += " AND edad = %s"
        filters.append(edad)
    if genero:
        query += " AND genero = %s"
        filters.append(genero)
    if ingreso_min:
        query += " AND ingreso_mensual >= %s"
        filters.append(ingreso_min)
    if ingreso_max:
        query += " AND ingreso_mensual <= %s"
        filters.append(ingreso_max)
    if saldo_min:
        query += " AND saldo_cuenta >= %s"
        filters.append(saldo_min)
    if saldo_max:
        query += " AND saldo_cuenta <= %s"
        filters.append(saldo_max)

    cursor.execute(query, filters)
    clientes = cursor.fetchall()
    total_filtrados = len(clientes)

    connection.close()
    return render_template('clientes.html', clientes=clientes, total_filtrados=total_filtrados)


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

@app.route('/datos')
def datos():
    clientes = obtener_clientes()
    prestamos = obtener_prestamos()
    transacciones = obtener_transacciones()
    fraudes = obtener_fraudes()
    pagos = obtener_pagos()

    return render_template(
        'datos.html', 
        clientes=clientes, 
        prestamos=prestamos, 
        transacciones=transacciones, 
        fraudes=fraudes, 
        pagos=pagos
    )

@app.route('/analisis')
def analisis():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Obtener datos de clientes
    cursor.execute("SELECT COUNT(*) AS total_clientes FROM clientes")
    total_clientes = cursor.fetchone()['total_clientes']

    # Obtener la distribución de préstamos
    cursor.execute("SELECT estado_prestamo, COUNT(*) AS cantidad FROM prestamos GROUP BY estado_prestamo")
    prestamos_estado = cursor.fetchall()

    # Obtener la distribución de fraudes
    cursor.execute("SELECT estado, COUNT(*) AS cantidad FROM fraudes GROUP BY estado")
    fraudes_estado = cursor.fetchall()

    # Obtener el flujo de transacciones
    cursor.execute("SELECT tipo_transaccion, SUM(monto) AS total FROM transacciones GROUP BY tipo_transaccion")
    transacciones_tipo = cursor.fetchall()

    connection.close()

    return render_template('analisis.html',
                           total_clientes=total_clientes,
                           prestamos_estado=prestamos_estado,
                           fraudes_estado=fraudes_estado,
                           transacciones_tipo=transacciones_tipo)
