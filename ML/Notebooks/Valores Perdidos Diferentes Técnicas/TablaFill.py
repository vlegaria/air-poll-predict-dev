import psycopg2
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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
    
    # Cargar datos de la tabla
    query = "SELECT * FROM apicalidadaire_uiz_norm;"
    data = pd.read_sql(query, conn)
    conn.close()

    # Visualizamos las primeras filas
    print(data.head())

except Exception as e:
    print(f"Error al conectarse a la base de datos: {e}")

# Relleno usando fillna() de Pandas (promedio de cada columna) para NaN y ceros
def fillna_imputation(df):
    df_with_zeros_as_nan = df.replace(0, float('nan'))
    return df_with_zeros_as_nan.fillna(df_with_zeros_as_nan.mean())

df_fillna_imputed = fillna_imputation(data.copy())
print("Datos después del relleno con fillna:")
print(df_fillna_imputed.head())
