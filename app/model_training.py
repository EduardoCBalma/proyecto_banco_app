import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from app.models import get_db_connection
import pickle
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Función para cargar los datos desde la base de datos
def cargar_datos():
    connection = get_db_connection()
    query = """
        SELECT edad, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, 
               cantidad_prestamos, monto_total_prestamos, estado_civil 
        FROM clientes
    """
    df = pd.read_sql(query, connection)
    connection.close()
    
    # Convertir variables categóricas a numéricas
    df['estado_civil'] = df['estado_civil'].map({'Soltero': 0, 'Casado': 1, 'Divorciado': 2, 'Viudo': 3})

    # Definir características (X) y variable objetivo (y)
    X = df.drop(columns=['estado_civil'])  # Se puede cambiar a otra variable objetivo si es necesario
    y = df['estado_civil']  # Se puede ajustar a la variable que se quiera predecir

    return X, y

# Preparar los datos para entrenamiento
def preparar_datos():
    X, y = cargar_datos()

    # División en conjunto de entrenamiento y prueba (80% entrenamiento, 20% prueba)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("\nTamaño del conjunto de entrenamiento:", X_train.shape)
    print("Tamaño del conjunto de prueba:", X_test.shape)

    return X_train, X_test, y_train, y_test

# Entrenamiento del modelo
def entrenar_modelo():
    X_train, X_test, y_train, y_test = preparar_datos()

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Evaluación del modelo
    y_pred = modelo.predict(X_test)
    print("Matriz de confusión:\n", confusion_matrix(y_test, y_pred))
    print("Reporte de clasificación:\n", classification_report(y_test, y_pred))
    print("Precisión del modelo:", accuracy_score(y_test, y_pred))

    # Guardar el modelo entrenado
    with open('app/model/modelo_riesgo.pkl', 'wb') as f:
        pickle.dump(modelo, f)

    print("Modelo guardado correctamente en 'app/model/modelo_riesgo.pkl'")

# Cargar el modelo previamente entrenado
def cargar_modelo():
    with open('app/model/modelo_riesgo.pkl', 'rb') as f:
        modelo = pickle.load(f)
    return modelo

# Función para predecir el riesgo de un cliente basado en los datos ingresados
def predecir_riesgo_cliente(datos_cliente):
    """
    Predice el riesgo del cliente basado en los datos ingresados.

    Args:
        datos_cliente (list): [edad, ingreso_mensual, saldo_cuenta, productos_contratados, historial_credito, 
                               cantidad_prestamos, monto_total_prestamos]

    Returns:
        str: "Alto riesgo" o "Bajo riesgo" según la predicción del modelo.
    """
    modelo = cargar_modelo()
    datos_cliente = np.array(datos_cliente).reshape(1, -1)
    prediccion = modelo.predict(datos_cliente)
    return "Alto riesgo" if prediccion[0] == 1 else "Bajo riesgo"

# Prueba local de predicción
if __name__ == "__main__":
    entrenar_modelo()
    datos_prueba = [30, 2500, 5000, 2, 7, 1, 15000]  # Datos ficticios para prueba
    resultado = predecir_riesgo_cliente(datos_prueba)
    print(f"Resultado de la predicción: {resultado}")
