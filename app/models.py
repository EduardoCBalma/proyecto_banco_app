import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='db5017039478.hosting-data.io',  # Nombre del host
        user='dbu2198138',  # Usuario de la base de datos
        password='Balma1989.@',  # Contraseña de la base de datos
        database='dbs13717170',  # Nombre de la base de datos
        port=3306  # Puerto estándar de MySQL
    )
