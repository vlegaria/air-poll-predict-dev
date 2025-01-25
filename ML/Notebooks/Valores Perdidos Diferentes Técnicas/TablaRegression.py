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

# Relleno usando regresión lineal para NaN y ceros
def linear_regression_imputation(df):
    df_imputed = df.copy()
    
    for column in df.columns:
        if df[column].isnull().any() or (df[column] == 0).any():
            df_column = df[column].replace(0, float('nan'))
            
            X = df.drop(columns=[column])
            y = df_column
            
            X_train = X[~y.isnull()]
            y_train = y.dropna()
            
            # Modelo de regresión lineal
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            missing_values = y.isnull() | (y == 0)
            df_imputed.loc[missing_values, column] = model.predict(X[missing_values])
    
    return df_imputed

# Rellenando con regresión lineal
df_linear_regression_imputed = linear_regression_imputation(data.copy())
print("Datos después del relleno con regresión lineal:")
print(df_linear_regression_imputed.head())
