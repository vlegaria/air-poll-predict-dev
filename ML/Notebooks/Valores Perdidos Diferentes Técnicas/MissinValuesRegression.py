import pandas as pd
import os
from sklearn.linear_model import LinearRegression

file_path = os.path.join("Dataset Original", "air_and_traffic_UIZ.csv")
data = pd.read_csv(file_path)
columns_to_process = ['CO', 'NO', 'NOX', 'NO2', 'O3', 'PM10', 'PM25', 'RH', 'SO2', 'TMP', 'WDR', 'WSP']

# Función para rellenar los valores 0 con regresión lineal
def fill_with_linear_regression(data, column_to_process, columns_to_use):
    mask = data[column_to_process] == 0
    if mask.sum() == 0: #Validacion, si no hay ceros no se ejecuta el algoritmo ahí 
        return data
    
    # Dividir en datos con valores conocidos y datos con valores faltantes (ceros)
    known_data = data[~mask]  
    missing_data = data[mask]  # Filas con ceros

    # Características y etiquetas para el modelo de regresión lineal
    X_known = known_data[columns_to_use]
    y_known = known_data[column_to_process]

    # Acá se entrena el modelo de regresión
    model = LinearRegression()
    model.fit(X_known, y_known)

    # Acá obtenemos los valores faltantes
    X_missing = missing_data[columns_to_use]
    predicted_values = model.predict(X_missing)

    # Se reeemplazan los valores que tenían cero
    data.loc[mask, column_to_process] = predicted_values
    
    return data

# Se hace un for para rellenar los valores cero de cada columna utilizando la regresión
for col in columns_to_process:
    columns_to_use = [col_ for col_ in columns_to_process if col_ != col]  # Usamos todas las otras columnas como características, es decir como indíces 
    data = fill_with_linear_regression(data, col, columns_to_use)

# Ruta para guardar el dataset procesado
processed_file_path = os.path.join("Dataset Original", "processed_air_and_traffic_UIZ_Regresion.csv")

# Se guarda el nuevo Dataset
data.to_csv(processed_file_path, index=False)

print(f"Archivo procesado con regresión lineal guardado en: {processed_file_path}")
