from app import app  # Importamos la instancia 'app' desde __init__.py
from flask import request, render_template, redirect, url_for, flash
import pandas as pd
from app.models import get_db_connection
from app.data_cleaning import limpiar_datos as limpiar_datos_script
from app.model_predict import predecir_cliente

@app.route('/upload_prestamos', methods=['POST'])
def upload_prestamos():
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
                INSERT INTO prestamos (cliente_id, monto_prestamo, tasa_interes, plazo_meses, historial_credito, pagos_atrasados, estado_prestamo, fecha_inicio, fecha_vencimiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['cliente_id'], row['monto_prestamo'], row['tasa_interes'], row['plazo_meses'],
                  row['historial_credito'], row['pagos_atrasados'], row['estado_prestamo'], row['fecha_inicio'], row['fecha_vencimiento']))

        connection.commit()
        connection.close()

        flash("Archivo de préstamos procesado correctamente", "success")
    except Exception as e:
        flash(f"Error al procesar el archivo: {e}", "error")

    return redirect(url_for('home'))

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

@app.route('/analisis')
def analisis():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            COUNT(*) AS total_clientes,
            COALESCE(SUM(saldo_cuenta), 0) AS saldo_total,
            COALESCE(AVG(edad), 0) AS promedio_edad,
            COALESCE(AVG(ingreso_mensual), 0) AS promedio_ingreso,
            COUNT(*) AS total_prestamos,
            COALESCE(SUM(monto_total_prestamos), 0) AS monto_total_prestamos,
            COALESCE(AVG(historial_credito), 0) AS promedio_historial_credito
        FROM clientes
    """)

    resumen = cursor.fetchone()
    connection.close()

    # Si no hay datos en la base, proporcionar valores por defecto
    if resumen is None:
        resumen = {
            'total_clientes': 0,
            'saldo_total': 0.0,
            'promedio_edad': 0,
            'promedio_ingreso': 0.0,
            'total_prestamos': 0,
            'monto_total_prestamos': 0.0,
            'promedio_historial_credito': 0.0
        }

    return render_template('analisis.html', resumen=resumen)
