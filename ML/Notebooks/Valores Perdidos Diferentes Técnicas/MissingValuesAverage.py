import pandas as pd
import os

# Ruta relativa al archivo de datos original
file_path = os.path.join("Dataset Original", "air_and_traffic_UIZ.csv")  
data = pd.read_csv(file_path)

# Columnas con valores NAN o 0 que deben ser procesadas
columns_to_process = ['CO', 'NO', 'NOX', 'NO2', 'O3', 'PM10', 'PM25', 'RH', 'SO2', 'TMP', 'WDR', 'WSP']

# Aquí rellenamos los valores NAN o 0 con el promedio de la columna
for col in columns_to_process:
    mean_value = data[data[col] != 0][col].mean()  # Excluir ceros al calcular el promedio
    data[col] = data[col].replace(0, mean_value)  # Reemplazar ceros por el promedio

# Ruta relativa para guardar el archivo procesado, en donde está el otro dataset
processed_file_path = os.path.join("Dataset Original", "air_and_traffic_UIZ_Average.csv")
data.to_csv(processed_file_path, index=False)
print(f"Archivo con promedios guardado en la ruta: {processed_file_path}")
