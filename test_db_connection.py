from app.models import get_db_connection

try:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    print(f"Conexión exitosa a la base de datos: {db_name[0]}")
    cursor.close()
    connection.close()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

