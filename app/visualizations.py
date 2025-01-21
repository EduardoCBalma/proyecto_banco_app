import matplotlib.pyplot as plt
import io
import base64
from app.models import get_db_connection
import pandas as pd

def generar_grafico_tendencias_prestamos():
    connection = get_db_connection()
    query = """
        SELECT DATE_FORMAT(fecha_inicio, '%Y-%m') AS mes, SUM(monto_prestamo) AS total_prestamos
        FROM prestamos
        GROUP BY mes
        ORDER BY mes
    """
    df = pd.read_sql(query, connection)
    connection.close()

    if df.empty:
        return None

    plt.figure(figsize=(8, 5))
    plt.plot(df['mes'], df['total_prestamos'], marker='o', linestyle='-')
    plt.xlabel('Mes')
    plt.ylabel('Monto Total de Préstamos')
    plt.title('Tendencia de Préstamos por Mes')
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    grafico_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return grafico_url
