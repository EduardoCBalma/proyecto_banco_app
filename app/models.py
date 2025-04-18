import mysql.connector
from app import db

import mysql.connector
from app import db

class Clientes(db.Model):
    __tablename__ = 'clientes'
    
    cliente_id = db.Column(db.Integer, primary_key=True, autoincrement=False)  # Eliminado autoincrement=True
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    genero = db.Column(db.String(10), nullable=False)
    ingreso_mensual = db.Column(db.Numeric(10, 2), nullable=True)
    saldo_cuenta = db.Column(db.Numeric(10, 2), nullable=True)
    productos_contratados = db.Column(db.Integer, nullable=True)
    historial_credito = db.Column(db.Integer, nullable=False)
    cantidad_prestamos = db.Column(db.Integer, nullable=False)
    monto_total_prestamos = db.Column(db.Numeric(10, 2), nullable=False)
    estado_civil = db.Column(db.String(50), nullable=False)
    ocupacion = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

class Prestamos(db.Model):
    __tablename__ = 'prestamos'
    
    prestamo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    monto_prestamo = db.Column(db.Numeric(10, 2), nullable=False)
    tasa_interes = db.Column(db.Float, nullable=False)
    plazo_meses = db.Column(db.Integer, nullable=False)
    historial_credito = db.Column(db.Integer, nullable=False)
    pagos_atrasados = db.Column(db.Integer, nullable=False)
    estado_prestamo = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)

class Pagos(db.Model):
    __tablename__ = 'pagos'
    
    pago_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prestamo_id = db.Column(db.Integer, nullable=False)
    monto_pagado = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)

class Fraudes(db.Model):
    __tablename__ = 'fraudes'
    
    fraude_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    monto_implicado = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_fraude = db.Column(db.Date, nullable=True)
    estado = db.Column(db.String(50), nullable=False)

class Transacciones(db.Model):
    __tablename__ = 'transacciones'
    
    transaccion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    tipo_transaccion = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_transaccion = db.Column(db.Date, nullable=False)
    categoria_transaccion = db.Column(db.String(50), nullable=False)

def get_db_connection():
    """Establece conexión con la base de datos remota."""
    connection = mysql.connector.connect(
        host='db4free.net',  # Anfitrión de la base de datos remota
        user='eduardocv',                # Usuario de la base de datos
        password='Balma2025!',             # Contraseña de la base de datos
        database='bancoappcv',             # Nombre de la base de datos
        port=3306,                         # Puerto de conexión
        autocommit=True
    )
    return connection

def crear_cliente(cliente_id, nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion):
    """Inserta un nuevo cliente en la base de datos."""
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO clientes (cliente_id, nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (cliente_id, nombre, edad, genero, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, cantidad_prestamos, monto_total_prestamos, estado_civil, ocupacion))
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

def obtener_pagos():
    """Obtiene la lista de pagos registrados."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pagos")
    pagos = cursor.fetchall()
    cursor.close()
    connection.close()
    return pagos
