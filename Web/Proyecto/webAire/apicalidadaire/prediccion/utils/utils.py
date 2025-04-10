from config.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np
from sklearn.metrics import make_scorer, mean_squared_error, r2_score, mean_absolute_error
from datetime import datetime, timedelta
import os
import torch
import torch.nn as nn
import numpy as np
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# === Modelo Autoencoder ===
class Autoencoder(nn.Module):
    def __init__(self, input_dim):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 8),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(8, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
def norm_df(df, scaler):
  #Si son negativos o vacios cambiarlos a nan
  for ind in range(df.shape[0]):
      for dato in df.columns:
          if(dato in ["CO", "NO",  "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", "traffic"]):
              if(df.loc[ind, dato] < 0):
                  df.loc[ind, dato] = np.nan

              if(df.loc[ind, dato] == ""):
                  df.loc[ind, dato] = np.nan
  month_idx= {12:4, 11:2, 10:1, 9:7, 8:6, 7:5, 6:9, 5:11, 4:10, 3:8, 2:12, 1:3}
  df["month_idx"] = df["month"].map(month_idx)

  hour_idx= {7:0, 6:1, 8:2, 5:3, 4:4, 9:5, 3:6, 2:7, 1:8, 0:9, 23:10, 22:11, 10:12, 21:13, 20:14, 19:15, 11:16, 18:17, 12:18, 17:19, 16:20, 13:21, 15:22, 14:23 }
  df["hour_idx"] = df["hour"].map(hour_idx)
  df = df.drop(columns=['month', 'hour',])
  df = df.rename(columns={'hour_idx': 'hour', 'month_idx':'month' })
  df_norm_data_escalada = df.copy()
  #Obtener los nuevos valores escalados
  # Normalizar
  df_norm_data_escalada[["CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", "month", "hour"]] = scaler.transform(df[["CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP","month", "hour"]])
  df_norm_data_escalada[['CO', 'NO', 'NOX', 'NO2', 'O3', 'PM10', 'PM25', 'RH', 'SO2','TMP', 'WDR', 'WSP', "month", "hour"]] = df_norm_data_escalada[['CO', 'NO', 'NOX', 'NO2', 'O3', 'PM10', 'PM25', 'RH', 'SO2','TMP', 'WDR', 'WSP', "month", "hour"]].round(12)
  return df_norm_data_escalada

def autoencoder_reconstruction(df, station):
    #with zipfile.ZipFile("autoencoder_model.keras.zip", "r") as zip_ref:
    #    zip_ref.extractall("autoencoder_model")
    print(os.getcwd())
    df["datetime"] = df["date"].astype(str) + " " + df["hour"].astype(str) +":00:00"
    df["datetime"] = pd.to_datetime(df["datetime"], format='%Y-%m-%d %H:%M:%S')
    dates = df["datetime"]
    df = df.drop_duplicates(subset='datetime', keep='first')
    month_hour = df[["traffic", "month", "hour"]]
    df = df.drop(columns=['idData', 'datetime', 'date', 'year', 'day','minutes', 'contingency', "traffic", "month", "hour"])
        
    # Crear la máscara de NaNs con las columnas ya limpias
    nan_mask = df.isna().values
    # Reemplazar NaNs con 0 solo en las columnas que se usan
    df_filled = df.fillna(0)
    X_np = df_filled.values
    # Luego lo conviertes a tensor float (usualmente se usa float32)
    X_tensor = torch.tensor(X_np, dtype=torch.float32)

    # Reconstrucción
    model = Autoencoder(12)  # Asegúrate de definir la clase antes
    if station =="UIZ":
        dir_encoder = "/home/sistema/www/air-poll-predict-dev/Web/Proyecto/webAire/apicalidadaire/prediccion/utils/autoencoder_pytorchUIZ.pth"
    if station =="MER":
        dir_encoder = "/home/sistema/www/air-poll-predict-dev/Web/Proyecto/webAire/apicalidadaire/prediccion/utils/autoencoder_pytorchMER.pth"
        
    model.load_state_dict(torch.load(dir_encoder, map_location=torch.device('cpu')))
    model.eval()
    with torch.no_grad():
        reconstructed_data = model(X_tensor).cpu().numpy()
    #return df_filled, reconstructed_data
    # Copiar los datos originales (ya normalizados con 0s)
    data_recon = df.copy().values
    # Reemplazar solo donde había NaNs
    data_recon[nan_mask] = reconstructed_data[nan_mask]

    # Opcional: convertir a DataFrame
    df_recon = pd.DataFrame(data_recon, columns=df.columns)
    df_recon = pd.concat([df_recon, month_hour], axis=1)
    df_recon = df_recon.clip(lower=0)
    return df_recon, dates

def table_data(table_name, target, station, scaler):
    # Crear la conexión
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos y cargar en un DataFrame
    #table_name = 'apicalidadaire_'+station+'_norm'
    query = f"SELECT * FROM {esquema}.{table_name};"
    df = pd.read_sql_query(query, engine)
    df.reset_index(drop=True, inplace=True)
    #df = df.dropna()
    #df.reset_index(drop=True, inplace=True)
    #df = norm_df(df, scaler)
    #dates = df.date
    df, dates = autoencoder_reconstruction(df, station)
    df = norm_df(df, scaler)
    y = df[target]
    #X = df.drop(columns=['idData', 'date', 'year', 'day','minutes', 'SO2', 'contingency'])
    X = df.drop(columns=['SO2', target])
    return X, y, df, dates

def ingest(df, target, time_steps):
    df = df.dropna()
    df = df.tail(time_steps)
    #X = df.drop(columns=['idData', 'date', 'year', 'day', 'minutes', 'SO2', 'contingency'])
    #X = X.drop(columns=[target])
    array = df.to_numpy()
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


def selectStatus(Status):
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos y cargar en un DataFrame
    table_name = 'apicalidadaire_estatuscalidad'
    query = f"SELECT * FROM {esquema}.{table_name} where \"idEstatus\" = {Status};"
    return pd.read_sql_query(query, engine)

def selectTarget(target):
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos y cargar en un DataFrame
    table_name = 'apicalidadaire_contaminantes'
    query = f"SELECT \"Contaminante\" FROM {esquema}.{table_name} where \"idContaminante\" = {target};"
    return pd.read_sql_query(query, engine)

def selectUnit(unit):
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos y cargar en un DataFrame
    table_name = 'apicalidadaire_unidades'
    query = f"SELECT \"descUnidad\" FROM {esquema}.{table_name} where \"idUnidad\" = {unit};"
    return pd.read_sql_query(query, engine)

def selectStation(station):
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos y cargar en un DataFrame
    table_name = 'apicalidadaire_estacionescame'
    query = f"SELECT * FROM {esquema}.{table_name} where \"idEstacion\" = {station};"
    return pd.read_sql_query(query, engine)

def registerPrediction(idStation,idContaminante,valorContaminante,idUnidad,idEstatus):
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    table_name = 'apicalidadaire_prediccion'
    query = f'INSERT INTO public.apicalidadaire_prediccion("Estacion_id", "Contaminante_id", "valorContaminante", "Unidad_id", "Estatus_id", "fechaPrediccion") VALUES ({idStation}, {idContaminante}, {valorContaminante}, {idUnidad}, {idEstatus}, CURRENT_TIMESTAMP );'

    with engine.connect() as conn:
       conn.execute(text(query))
       conn.commit()

    query = f"SELECT \"idPrediccion\" FROM {esquema}.{table_name} where \"Estacion_id\" = {idStation} and \"Contaminante_id\" = {idContaminante} and \"valorContaminante\" = {valorContaminante} and \"Unidad_id\" = {idUnidad} and \"Estatus_id\" = {idEstatus} ORDER BY \"fechaPrediccion\" DESC LIMIT 1;"
    return pd.read_sql_query(query, engine)


def selectUltimasPredic(idstation):
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos y cargar en un DataFrame
    table_name = 'apicalidadaire_prediccion'
    query = f"SELECT * FROM {esquema}.{table_name} where \"Estacion_id\" = {idstation} order by \"idPrediccion\" desc limit 100;"
    print(query)
    predicciones = pd.read_sql_query(query, engine)

    predicciones.dropna()

    fechaObtener = datetime.now() + timedelta(days=5)

    prediccionesPorHora = pd.DataFrame(columns=predicciones.columns)

    horaAgregada = False

    for indPred in range(predicciones.shape[0]):

        fechaPred = predicciones.loc[indPred,"fechaPrediccion"].to_pydatetime()

        #print(f'fechaPred: {fechaPred} fechaObtener: {fechaObtener}')

        if(not( fechaObtener.hour == fechaPred.hour and fechaObtener.day == fechaPred.day and fechaObtener.month == fechaPred.month and fechaObtener.year == fechaPred.year)):
            horaAgregada = False

        while (not (fechaObtener.hour == fechaPred.hour and fechaObtener.day == fechaPred.day and fechaObtener.month == fechaPred.month and fechaObtener.year == fechaPred.year)):

            fechaObtener = fechaObtener  - timedelta(hours=1)

        if(fechaObtener.hour == fechaPred.hour and fechaObtener.day == fechaPred.day and fechaObtener.month == fechaPred.month and fechaObtener.year == fechaPred.year):

            if( not horaAgregada ):

                prediccionesPorHora = pd.concat([prediccionesPorHora, predicciones.iloc[[indPred]]], ignore_index=True)

                horaAgregada = True

        if(prediccionesPorHora.shape[0] == 30):
            break

    return prediccionesPorHora


def selectUltimosDatos(station, ultimasPred):
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos y cargar en un DataFrame
    table_name = f'apicalidadaire_{station}_prom_hr'
    query = f"SELECT * FROM {esquema}.{table_name} order by \"idData\" desc limit 100;"
    print(query)
    registros =  pd.read_sql_query(query, engine)

    indexPred = 0

    dicPredVal = []

    for indPred in range(ultimasPred.shape[0]):

        fechaPred = ultimasPred.loc[indPred,"fechaPrediccion"].to_pydatetime() - timedelta(days=1)

        regDePred = registros[(registros['hour'] == fechaPred.hour) & (registros['day'] == fechaPred.day)]

        #print(regDePred)

        if(regDePred.shape[0] > 0 ):

            #print(regDePred["O3"].to_list()[0])

            if(not str(regDePred["O3"].to_list()[0]) == "nan" and indexPred < 10 ):

                #print("Agregar registro")

                dicPredVal.append([fechaPred.strftime("%Y-%m-%d %H:%M:%S"), regDePred["O3"].to_list()[0],ultimasPred.loc[indPred,"valorContaminante"]])

                indexPred = indexPred + 1

        if(indexPred == 10):
            break

    print(dicPredVal)

    return dicPredVal