import pandas as pd

#Ruta al dataset
file_path = "C:\\Users\\User\\OneDrive\\Documentos\\GitHub\\Portafolio\\air-poll-predict-dev\\ML\\Notebooks\Valores Perdidos Diferentes Técnicas\\Dataset Original\\air_and_traffic_UIZ.csv"  
data = pd.read_csv(file_path)

#Columnas con presencia de valores NAN o 0, e n este caso no nos convienen, peuden afectar el accuracy
columns_to_process = ['CO', 'NO', 'NOX', 'NO2', 'O3', 'PM10', 'PM25', 'RH', 'SO2', 'TMP', 'WDR', 'WSP']

# Rellenando valores 0 o NAN  con el promedio de la columna, acá el cero nos puede afectar por lo que ignoraremos esa lectura
for col in columns_to_process: #Hacemos un for  para rellenar los ceros en las columnas
    mean_value = data[data[col] != 0][col].mean()  # Aquí vamos a calcular el promedio de la columna pero excluyendo ceros
    data[col] = data[col].replace(0, mean_value)  # Rellenar ceros con el promedio calculado, usando replace

# Guardar el dataset procesado
processed_file_path = "C:\\Users\\User\\OneDrive\\Documentos\\GitHub\\Portafolio\\air-poll-predict-dev\\ML\\Notebooks\\Valores Perdidos Diferentes Técnicas"
data.to_csv(processed_file_path, index=False)

print(f"Archivo procesado guardado en: {processed_file_path}")
