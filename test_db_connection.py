from app.models import get_db_connection

try:
    connection = get_db_connection()
    print("¡Conexión exitosa a la base de datos!")
    connection.close()
except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")
