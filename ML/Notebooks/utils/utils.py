from config.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sklearn.metrics import make_scorer, mean_squared_error, r2_score, mean_absolute_error

def table_data(table_name, target, station):
    # Crear la conexión
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos y cargar en un DataFrame
    table_name = 'apicalidadaire_'+station+'_norm'
    query = f"SELECT * FROM {esquema}.{table_name};"
    df = pd.read_sql_query(query, engine)
    print(len(df))
    dates = df.date
    df = df.dropna().reset_index(drop=True)
    y = df[target]
    X = df.drop(columns=['idData', 'date', 'year', 'month', 'day', 'hour', 'minutes', 'NOX'])
    X = X.drop(columns=[target])
    return X, y, df, dates

def ingest(df, target, time_steps):
    df = df.tail(time_steps)
    X = df.drop(columns=['idData', 'date', 'year', 'month', 'day', 'hour', 'minutes', 'NOX'])
    X = X.drop(columns=[target])
    array = X.to_numpy()
    vector = array.flatten()
    return np.array([vector])

def create_sequences2(X, y, time_steps, time_future):
  Xs, ys = [], []
  for i in range(len(X) - time_steps-time_future):
    df = X[i:(i + time_steps)]
    array = df.to_numpy()
    # Aplanar el array a un vector
    vector = array.flatten()
    Xs.append(vector)
    ys.append(y[i + time_steps+time_future])
  return np.array(Xs), np.array(ys)

def metrics(X, y_test, predicciones, printData):
    n = len(y_test)
    p = X.shape[1]
    # Coeficiente de determinación (R-cuadrado)
    r2 = r2_score(y_test, predicciones)
    # R-cuadrado ajustado
    r2_adjusted = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    # Error cuadrado medio
    rmse = mean_squared_error(y_true  = y_test, y_pred  = predicciones, squared = False)
    # Error Absoluto Medio
    mae = mean_absolute_error(y_test, predicciones)
    
    r2 = round(r2, 6)
    r2_adjusted = round(r2_adjusted, 6)
    rmse = round(rmse, 6)
    mae = round(mae, 6)
    if printData:
      print("R^2:", r2)
      print("R^2 ajustado:", r2_adjusted)
      print("RMSE", rmse)
      print("MAE:", mae)
    return {'r2':r2, 'r2adjusted':r2_adjusted,'rmse': rmse, 'mae':mae}

