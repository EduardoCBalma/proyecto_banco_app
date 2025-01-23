from app import app  # Importamos la instancia 'app' desde __init__.py
from flask import request, render_template, redirect, url_for, flash
import pandas as pd
from app.models import get_db_connection
from app.data_cleaning import limpiar_datos as limpiar_datos_script
from app.model_predict import predecir_cliente
from app.models import Clientes
from flask import render_template
from app.models import obtener_clientes, obtener_prestamos, obtener_transacciones, obtener_fraudes, obtener_pagos
from datetime import datetime

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

        # Verificación de valores nulos
        if df.isnull().values.any():
            flash("El archivo contiene valores nulos", "error")
            return redirect(url_for('home'))

        # Convertir fechas al formato correcto para MySQL (yyyy-mm-dd)
        df['fecha_pago'] = pd.to_datetime(df['fecha_pago'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')

        # Verificar si hay errores en la conversión de fecha
        if df['fecha_pago'].isnull().any():
            flash("Error en el formato de fecha, debe ser dd/mm/yyyy", "error")
            return redirect(url_for('home'))

        connection = get_db_connection()
        cursor = connection.cursor()

        for index, row in df.iterrows():
            cursor.execute("SELECT prestamo_id FROM prestamos WHERE prestamo_id = %s", (row['prestamo_id'],))
            resultado = cursor.fetchone()

            if not resultado:
                print(f"Error: préstamo ID {row['prestamo_id']} no existe en la base de datos.")
                continue  # Saltar esta fila

            # Inserción si el ID existe
            cursor.execute("""
                INSERT INTO pagos (prestamo_id, monto_pagado, fecha_pago, metodo_pago) 
                VALUES (%s, %s, %s, %s)
            """, (
                row['prestamo_id'],
                row['monto_pagado'],
                row['fecha_pago'],
                row['metodo_pago']
            ))

        connection.commit()
        cursor.close()
        connection.close()

        flash("Archivo de pagos procesado correctamente", "success")

    except Exception as e:
        flash(f"Error al procesar el archivo de pagos: {e}", "error")

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

    try:
        # Resumen de clientes
        cursor.execute("SELECT COUNT(*) AS total_clientes FROM clientes")
        total_clientes = cursor.fetchone().get('total_clientes', 0)

        cursor.execute("SELECT COALESCE(SUM(saldo_cuenta), 0) AS saldo_total FROM clientes")
        saldo_total = cursor.fetchone().get('saldo_total', 0)

        cursor.execute("SELECT COALESCE(AVG(edad), 0) AS promedio_edad FROM clientes")
        promedio_edad = cursor.fetchone().get('promedio_edad', 0)

        cursor.execute("SELECT COALESCE(AVG(ingreso_mensual), 0) AS promedio_ingreso FROM clientes")
        promedio_ingreso = cursor.fetchone().get('promedio_ingreso', 0)

        # Resumen de préstamos
        cursor.execute("SELECT COUNT(*) AS total_prestamos FROM prestamos")
        total_prestamos = cursor.fetchone().get('total_prestamos', 0)

        cursor.execute("SELECT COALESCE(SUM(monto_prestamo), 0) AS monto_total_prestamos FROM prestamos")
        monto_total_prestamos = cursor.fetchone().get('monto_total_prestamos', 0)

        cursor.execute("SELECT COALESCE(AVG(tasa_interes), 0) AS promedio_tasa_interes FROM prestamos")
        promedio_tasa_interes = cursor.fetchone().get('promedio_tasa_interes', 0)

        cursor.execute("""
            SELECT 
                COUNT(*) AS total_prestamos, 
                SUM(CASE WHEN pagos_atrasados > 0 THEN 1 ELSE 0 END) AS prestamos_en_mora,
                (SUM(CASE WHEN pagos_atrasados > 0 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS porcentaje_mora
            FROM prestamos
        """)
        resultados_mora = cursor.fetchone()

        total_prestamos = resultados_mora.get('total_prestamos', 0)
        prestamos_en_mora = resultados_mora.get('prestamos_en_mora', 0)
        porcentaje_mora = resultados_mora.get('porcentaje_mora', 0)

        connection.close()

        # Pasar datos a la plantilla
        return render_template('analisis.html',
                               total_clientes=total_clientes,
                               saldo_total=saldo_total,
                               promedio_edad=promedio_edad,
                               promedio_ingreso=promedio_ingreso,
                               total_prestamos=total_prestamos,
                               monto_total_prestamos=monto_total_prestamos,
                               promedio_tasa_interes=promedio_tasa_interes,
                               prestamos_en_mora=prestamos_en_mora)
    except Exception as e:
        connection.close()
        return f"Error al obtener datos de análisis: {str(e)}"
    
@app.route('/analisis_dashboard')
def dashboard_analisis():
    return render_template('analisis.html', fecha_actual=datetime.now().strftime('%d/%m/%Y'))

