import psycopg2
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Parámetros de la base de datos
DB_NAME = 'calidadAire'
DB_USER = 'postgres'
DB_PASSWORD = 'rafael1995'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Conexión a la base de datos
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Conexión exitosa a la base de datos.")
    query = "SELECT * FROM apicalidadaire_uiz_norm;"
    data = pd.read_sql(query, conn)
    conn.close()
    print(data.head())

except Exception as e:
    print(f"Error al conectarse a la base de datos: {e}")

# Relleno usando KNN (K-Nearest Neighbors) para NaN y ceros
def knn_imputation(df):
    df_with_zeros_as_nan = df.replace(0, float('nan')) 
    imputer = KNNImputer(n_neighbors=5)
    df_imputed = pd.DataFrame(imputer.fit_transform(df_with_zeros_as_nan), columns=df.columns)
    
    return df_imputed

df_knn_imputed = knn_imputation(data.copy())
print("Datos después del relleno con KNN:")
print(df_knn_imputed.head())
