import pandas as pd
from sqlalchemy import text
from app.models import get_db_connection

def limpiar_datos():
    try:
        # Conexión con la base de datos
        connection = get_db_connection()

        # Leer los datos de la tabla 'clientes'
        query = "SELECT * FROM clientes"
        df = pd.read_sql(query, connection)

        # Llenar valores nulos con valores predeterminados
        df.fillna({
            'ingreso_mensual': 0.0,
            'saldo_cuenta': 0.0,
            'productos_contratados': 0,
            'historial_credito': 0,
            'cantidad_prestamos': 0,
            'monto_total_prestamos': 0.0,
            'estado_civil': 'Desconocido',
            'ocupacion': 'Desconocida'
        }, inplace=True)

        total_antes = len(df)

        # Eliminar registros duplicados
        df.drop_duplicates(subset=['cliente_id', 'nombre', 'edad', 'genero', 'saldo_cuenta'], inplace=True)

        # Eliminar registros con valores nulos en columnas clave
        df.dropna(inplace=True)

        # Corregir valores negativos
        numeric_columns = ['ingreso_mensual', 'saldo_cuenta', 'monto_total_prestamos']
        df[numeric_columns] = df[numeric_columns].abs()

        # Filtrar registros con edades irreales (<18 años)
        df = df[df['edad'] >= 18]

        total_despues = len(df)

        # Preparar consulta para actualización
        update_query = text("""
            UPDATE clientes 
            SET 
                ingreso_mensual = :ingreso_mensual, 
                saldo_cuenta = :saldo_cuenta, 
                productos_contratados = :productos_contratados, 
                historial_credito = :historial_credito, 
                cantidad_prestamos = :cantidad_prestamos, 
                monto_total_prestamos = :monto_total_prestamos, 
                estado_civil = :estado_civil, 
                ocupacion = :ocupacion 
            WHERE cliente_id = :cliente_id
        """)

        data_to_update = df[['ingreso_mensual', 'saldo_cuenta', 'productos_contratados',
                             'historial_credito', 'cantidad_prestamos', 'monto_total_prestamos',
                             'estado_civil', 'ocupacion', 'cliente_id']].to_dict(orient='records')

        # Ejecutar actualizaciones
        with connection.cursor() as cursor:
            for row in data_to_update:
                cursor.execute(update_query, row)

        connection.commit()
        connection.close()

        print(f"✅ Datos antes de la limpieza: {total_antes}")
        print(f"✅ Datos después de la limpieza: {total_despues}")

        return total_antes, total_despues

    except Exception as e:
        print(f"❌ Error al limpiar los datos: {e}")
        return None

if __name__ == "__main__":
    limpiar_datos()

