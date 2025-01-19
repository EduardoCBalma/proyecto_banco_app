from app.models import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    database_name = cursor.fetchone()
    print(f"Conectado a la base de datos: {database_name[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error al conectar: {e}")
