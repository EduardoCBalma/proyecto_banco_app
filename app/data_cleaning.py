import pandas as pd
from app.models import get_db_connection

def limpiar_datos():
    connection = get_db_connection()
    query = "SELECT * FROM clientes"
    df = pd.read_sql(query, connection)

    total_antes = len(df)

    # Eliminar registros duplicados
    df.drop_duplicates(subset=['nombre', 'edad', 'genero', 'saldo_cuenta'], inplace=True)

    # Eliminar registros con valores nulos
    df.dropna(inplace=True)

    # Corregir valores negativos en campos numéricos
    df['ingreso_mensual'] = df['ingreso_mensual'].abs()
    df['saldo_cuenta'] = df['saldo_cuenta'].abs()
    df['monto_total_prestamos'] = df['monto_total_prestamos'].abs()

    # Filtrar registros con edades irreales
    df = df[df['edad'] >= 18]

    total_despues = len(df)

    # Actualizar la base de datos sin borrar la tabla
    cursor = connection.cursor()

    for index, row in df.iterrows():
        cursor.execute("""
            UPDATE clientes 
            SET 
                ingreso_mensual = %s, 
                saldo_cuenta = %s, 
                productos_contratados = %s, 
                historial_credito = %s, 
                cantidad_prestamos = %s, 
                monto_total_prestamos = %s, 
                estado_civil = %s, 
                ocupacion = %s 
            WHERE cliente_id = %s
        """, (
            row['ingreso_mensual'], row['saldo_cuenta'], row['productos_contratados'], 
            row['historial_credito'], row['cantidad_prestamos'], row['monto_total_prestamos'], 
            row['estado_civil'], row['ocupacion'], row['cliente_id']
        ))

    connection.commit()
    connection.close()

    return total_antes, total_despues

if __name__ == "__main__":
    limpiar_datos()
