import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='db5017038622.hosting-data.io',  # Por ejemplo: db12345678.hosting-data.io
        user='dbu2178344',  # Usuario configurado
        password='Balma1989.@',  # Contraseña configurada
        database='banco_app',  # Nombre de la base de datos
        port=3306  # Puerto estándar de MySQL
    )
