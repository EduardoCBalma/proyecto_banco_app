import mysql.connector

def get_db_connection():
    """Establece conexión con la base de datos local MySQL."""
    connection = mysql.connector.connect(
        host='localhost',      # Cambiar si se necesita conectar a un servidor remoto en el futuro
        user='root',           # Usuario de MySQL Workbench
        password='171189',  # Reemplaza con tu contraseña local
        database='banco_app',  # Nombre de la base de datos
        autocommit=True
    )
    return connection

def crear_cliente(nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion):
    """Inserta un nuevo cliente en la base de datos."""
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO clientes (nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion))
    connection.commit()
    cursor.close()
    connection.close()

def obtener_clientes():
    """Obtiene la lista de clientes registrados."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    connection.close()
    return clientes

def crear_prestamo(cliente_id, monto_prestamo, tasa_interes, plazo_meses, historial_credito, pagos_atrasados, estado_prestamo, fecha_inicio, fecha_vencimiento):
    """Inserta un nuevo préstamo en la base de datos."""
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO prestamos (cliente_id, monto_prestamo, tasa_interes, plazo_meses, historial_credito, pagos_atrasados, estado_prestamo, fecha_inicio, fecha_vencimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (cliente_id, monto_prestamo, tasa_interes, plazo_meses, historial_credito, pagos_atrasados, estado_prestamo, fecha_inicio, fecha_vencimiento))
    connection.commit()
    cursor.close()
    connection.close()

def obtener_prestamos():
    """Obtiene la lista de préstamos registrados."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prestamos")
    prestamos = cursor.fetchall()
    cursor.close()
    connection.close()
    return prestamos

def crear_transaccion(cliente_id, tipo_transaccion, monto, categoria_transaccion):
    """Registra una nueva transacción bancaria."""
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO transacciones (cliente_id, tipo_transaccion, monto, categoria_transaccion)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (cliente_id, tipo_transaccion, monto, categoria_transaccion))
    connection.commit()
    cursor.close()
    connection.close()

def obtener_transacciones():
    """Obtiene la lista de transacciones registradas."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transacciones")
    transacciones = cursor.fetchall()
    cursor.close()
    connection.close()
    return transacciones

def registrar_fraude(cliente_id, descripcion, monto_implicado, estado):
    """Registra un posible fraude detectado."""
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO fraudes (cliente_id, descripcion, monto_implicado, estado)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (cliente_id, descripcion, monto_implicado, estado))
    connection.commit()
    cursor.close()
    connection.close()

def obtener_fraudes():
    """Obtiene la lista de fraudes registrados."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fraudes")
    fraudes = cursor.fetchall()
    cursor.close()
    connection.close()
    return fraudes
