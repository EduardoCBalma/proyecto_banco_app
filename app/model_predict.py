import pickle
import numpy as np

# Cargar el modelo entrenado
def cargar_modelo():
    with open('app/models/modelo_entrenado.pkl', 'rb') as file:
        modelo = pickle.load(file)
    return modelo

def predecir_cliente(datos_cliente):
    modelo = cargar_modelo()
    # Convertir los datos a un arreglo numpy
    datos_array = np.array([[
        datos_cliente['edad'],
        datos_cliente['ingreso_mensual'],
        datos_cliente['saldo_cuenta'],
        datos_cliente['productos_contratados'],
        datos_cliente['historial_credito'],
        datos_cliente['cantidad_prestamos'],
        datos_cliente['monto_total_prestamos']
    ]])
    # Realizar la predicción (1: riesgo alto, 0: riesgo bajo)
    prediccion = modelo.predict(datos_array)
    probabilidad = modelo.predict_proba(datos_array)[0][1]  # Probabilidad de impago
    return prediccion[0], probabilidad
