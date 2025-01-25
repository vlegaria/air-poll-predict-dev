import pandas as pd
import os
from sklearn.impute import KNNImputer
file_path = os.path.join("Dataset Original", "air_and_traffic_UIZ.csv")
data = pd.read_csv(file_path)
columns_to_process = ['CO', 'NO', 'NOX', 'NO2', 'O3', 'PM10', 'PM25', 'RH', 'SO2', 'TMP', 'WDR', 'WSP']

# Función para rellenar valores con KNN
def fill_with_knn(data, columns_to_process, n_neighbors=5):
    # Inicializar el imputer KNN
    knn_imputer = KNNImputer(n_neighbors=n_neighbors)
    data[columns_to_process] = knn_imputer.fit_transform(data[columns_to_process])
    
    return data

# Rellenar los valores usando los KNN calculados
data = fill_with_knn(data, columns_to_process)

# Ruta ya saben para qué
processed_file_path = os.path.join("Dataset Original", "processed_air_and_traffic_UIZ_with_knn.csv")
data.to_csv(processed_file_path, index=False)
print(f"Archivo procesado con el método KNN guardado en: {processed_file_path}")
