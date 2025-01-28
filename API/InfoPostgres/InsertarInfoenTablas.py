from config.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np
import mlflow
from mlflow.tracking import MlflowClient
import pickle
import warnings
from datetime import date

# Ignorar todos los warnings
warnings.filterwarnings("ignore")

#Cargar cliente mlfow
mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
client = MlflowClient()
import os

#Conexión a la base de datos

engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
esquema = 'public'
table_name = 'apicalidadaire_prediccion'

#Insertar datos de Mer_Norm


def InsertarDatosMer():
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_traffic_MER_norm.csv')
    mer = pd.read_csv(ruta_csv)
    #mer = pd.read_csv('Datos/air_traffic_MER.csv')

    for ind in range(mer.shape[0]):
        
        #Query de insert
        query = f'INSERT INTO public."apicalidadaire_mer_norm" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic) VALUES (\'{mer.loc[ind, "date"][0:10]}\',{mer.loc[ind, "CO"]},{mer.loc[ind, "NO"]},{mer.loc[ind, "NOX"]},{mer.loc[ind, "NO2"]},{mer.loc[ind, "O3"]},{mer.loc[ind, "PM10"]},{mer.loc[ind, "PM25"]},{mer.loc[ind, "RH"]},{mer.loc[ind, "SO2"]},{mer.loc[ind, "TMP"]},{mer.loc[ind, "WDR"]},{mer.loc[ind, "WSP"]},{mer.loc[ind, "year"]},{mer.loc[ind, "month"]},{mer.loc[ind, "day"]},{mer.loc[ind, "hour"]},{mer.loc[ind, "minute"]},{mer.loc[ind, "traffic"]});'
        
        query = query.replace("nan","\'nan\'")
        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def InsertarDatosUiz():
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_traffic_UIZ_norm.csv')
    uiz = pd.read_csv(ruta_csv)
    #uiz = pd.read_csv('Datos/air_and_traffic_UIZ.csv')

    for ind in range(uiz.shape[0]):

        #Query de insert
        query = f'INSERT INTO public."apicalidadaire_uiz_norm" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic) VALUES (\'{uiz.loc[ind, "date"][0:10]}\',{uiz.loc[ind, "CO"]},{uiz.loc[ind, "NO"]},{uiz.loc[ind, "NOX"]},{uiz.loc[ind, "NO2"]},{uiz.loc[ind, "O3"]},{uiz.loc[ind, "PM10"]},{uiz.loc[ind, "PM25"]},{uiz.loc[ind, "RH"]},{uiz.loc[ind, "SO2"]},{uiz.loc[ind, "TMP"]},{uiz.loc[ind, "WDR"]},{uiz.loc[ind, "WSP"]},{uiz.loc[ind, "year"]},{uiz.loc[ind, "month"]},{uiz.loc[ind, "day"]},{uiz.loc[ind, "hour"]},{uiz.loc[ind, "minute"]},{uiz.loc[ind, "traffic"]});'

        query = query.replace("nan","\'nan\'")
        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def InsertarDatosEstaciones():
    #estaciones = pd.read_csv('Datos/estacionesCAME.csv')
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'estacionesCAME.csv')
    estaciones = pd.read_csv(ruta_csv)
    for ind in range(estaciones.shape[0]):
        fecha = f'{estaciones.loc[ind, "date"][6:]}-{estaciones.loc[ind, "date"][3:5]}-{estaciones.loc[ind, "date"][:2]}'

        #A los valores númericos vacios les pongo null
        O3 = int(estaciones.loc[ind, "O3"]) if not np.isnan(estaciones.loc[ind, "O3"]) else "null"
        CO = int(estaciones.loc[ind, "CO"]) if not np.isnan(estaciones.loc[ind, "CO"]) else "null"
        SO2 = int(estaciones.loc[ind, "SO2"]) if not np.isnan(estaciones.loc[ind, "SO2"]) else "null"
        NO2 = int(estaciones.loc[ind, "NO2"]) if not np.isnan(estaciones.loc[ind, "NO2"]) else "null"
        PM10 = int(estaciones.loc[ind, "PM10"]) if not np.isnan(estaciones.loc[ind, "PM10"]) else "null"
        PM25 = int(estaciones.loc[ind, "PM25"]) if not np.isnan(estaciones.loc[ind, "PM25"]) else "null"

        query = f'INSERT INTO public."apicalidadaire_estacionescame" ( key, name, "ID", "O3", "CO", "SO2", "NO2", "PM10", "PM25", status, date, municipality, state, altitude, latitude, longitude, address, website, notes, traffic, "xTileIn", "yTileIn") VALUES (\'{estaciones.loc[ind, "Key"]}\', \'{estaciones.loc[ind, "Name"]}\', \'{int(estaciones.loc[ind, "ID"])}\', {O3}, {CO}, {SO2}, {NO2}, {PM10}, {PM25}, \'{estaciones.loc[ind, "Status"]}\', \'{fecha}\', \'{estaciones.loc[ind, "Alcaldía o municipio"]}\', \'{estaciones.loc[ind, "State"]}\', \'{estaciones.loc[ind, "Altitud (msnm)"]}\', \'{estaciones.loc[ind, "Latitude"]}\', \'{estaciones.loc[ind, "Longitude"]}\', \'{estaciones.loc[ind, "Domicilio"]}\', \'{estaciones.loc[ind, "Página"]}\', \'{estaciones.loc[ind, "Notas"]}\', \'{estaciones.loc[ind, "Trafico"]}\', \'{estaciones.loc[ind, "xTile_in"]}\', \'{estaciones.loc[ind, "yTile_in"]}\');'

        query = query.replace('nan','')

         #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def InsertarDatosMerHr():
    mer = pd.read_csv('Datos/MER_prom_hr_sin_negativos.csv')

    for ind in range(mer.shape[0]):

        dateHour = mer.loc[ind, "date"]

        #datos de fecha
        dateHourSep = dateHour.split(" ")
        date = dateHourSep[0]
        time = dateHourSep[1]

        dateSep = date.split("/")
        year = dateSep[0]
        month = int(dateSep[1])
        day = int(dateSep[2])

        timeSep = time.split(":")
        hour = int(timeSep[0])
        minute = int(timeSep[1])


        #Query de insert
        query = f"""INSERT INTO public."apicalidadaire_mer_prom_hr" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic, contingency) VALUES (\'{year}-{dateSep[1]}-{dateSep[2]}\',
                {mer.loc[ind, "CO"]},{mer.loc[ind, "NO"]},{mer.loc[ind, "NOX"]},{mer.loc[ind, "NO2"]},{mer.loc[ind, "O3"]},{mer.loc[ind, "PM10"]},{mer.loc[ind, "PM25"]},{mer.loc[ind, "RH"]},{mer.loc[ind, "SO2"]},{mer.loc[ind, "TMP"]},{mer.loc[ind, "WDR"]},{mer.loc[ind, "WSP"]},{year},{month},{day},{hour},{minute},{np.nan},0);"""

        query = query.replace("nan","\'nan\'")

        #print(query)
        
        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def InsertarDatosUizHr():
    #uiz = pd.read_csv('Datos/UIZ_prom_hr_sin_negativos.csv')
     
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_traffic_UIZ_prom.csv')
    uiz = pd.read_csv(ruta_csv)

    for ind in range(uiz.shape[0]):
        dateHour = uiz.loc[ind, "date"]

        #datos de fecha
        dateHourSep = dateHour.split(" ")
        date = dateHourSep[0]
        time = dateHourSep[1]

        dateSep = date.split("/")
        year = dateSep[0]
        month = int(dateSep[1])
        day = int(dateSep[2])

        timeSep = time.split(":")
        hour = int(timeSep[0])
        minute = int(timeSep[1])
        #Query de insert
        query = f"""INSERT INTO public."apicalidadaire_uiz_prom_hr" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic, contingency) VALUES (\'{year}-{dateSep[1]}-{dateSep[2]}\',
                {uiz.loc[ind, "CO"]},{uiz.loc[ind, "NO"]},{uiz.loc[ind, "NOX"]},{uiz.loc[ind, "NO2"]},{uiz.loc[ind, "O3"]},{uiz.loc[ind, "PM10"]},{uiz.loc[ind, "PM25"]},{uiz.loc[ind, "RH"]},{uiz.loc[ind, "SO2"]},{uiz.loc[ind, "TMP"]},{uiz.loc[ind, "WDR"]},{uiz.loc[ind, "WSP"]},{year},{month},{day},{hour},{minute},{np.nan},0);"""
        query = query.replace("nan","\'nan\'")

        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def NormDatosHr():
    stations2forecast = ['mer','uiz']

    for station in stations2forecast:

        #Obtener scaler
        model_name = "O3-"+str(station.lower())+"_24hr_forecast_model"
        best_model_alias = "champion"

        best_model_info = client.get_model_version_by_alias(model_name, best_model_alias)
        best_model_run_id = best_model_info.run_id

        scaler_dir = 'artifacts/'+station.upper()+'_scaler.pkl'
        local_path = mlflow.artifacts.download_artifacts(run_id=best_model_run_id, artifact_path=scaler_dir)

        with open(local_path, "rb") as f:
            scaler = pickle.load(f)

        engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        esquema = 'public'
        

        table_name = 'apicalidadaire_'+station+'_norm'

        #Seleccionar registro mas nuevo norm
        query = f"SELECT * FROM {esquema}.{table_name} order by date desc limit 1;"

        dfnormReciente = pd.read_sql_query(query, engine)

        #Seleccionar registro mas antiguo norm
        query = f"SELECT * FROM {esquema}.{table_name} order by date limit 1;"

        dfnormAnt= pd.read_sql_query(query, engine)
        
		# Recuperar los datos de la hora con fechas mayor a la mas nueva y menor a la mas antigua y cargar en un DataFrame
        table_name = 'apicalidadaire_'+station+'_prom_hr'
        query = f"SELECT * FROM {esquema}.{table_name} where date > '{dfnormReciente.iloc[0].date}' or date < '{dfnormAnt.iloc[0].date}';"
        print(query)

        dfHourFuera = pd.read_sql_query(query, engine)

        #Normalizar datos 

        if len(dfHourFuera)>0:

            dfHourFuera_escalado = dfHourFuera.copy()

            dfHourFuera_escalado[["CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]] = scaler.transform(dfHourFuera[["CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]])

            #Probe y para los datos no es necesario el escalado, por lo que no contemplare ese caso al tratarse de una unica ejecución 

            dfHourFuera_escalado = dfHourFuera_escalado.applymap(lambda x: "nan" if pd.isna(x) else x)

            dfHourFuera_escalado = dfHourFuera_escalado.drop(columns=['idData'])

            table_name = 'apicalidadaire_'+station+'_norm'

            dfHourFuera_escalado.to_sql(table_name, engine, if_exists='append', method='multi', index=False)

        # Recuperar los datos dentro de las fechas y cargar en un DataFrame
        table_name = 'apicalidadaire_'+station+'_prom_hr'
        query = f"SELECT * FROM {esquema}.{table_name} where not (date > '{dfnormReciente.iloc[0].date}' or date < '{dfnormAnt.iloc[0].date}');"
        print(query)

        dfHourDentro = pd.read_sql_query(query, engine)

        if len(dfHourDentro)>0:

            dfHourDentro_escalado = dfHourDentro.copy()

            dfHourDentro_escalado[["CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]] = scaler.transform(dfHourDentro[["CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]])
            
            dfDatosNuevos = pd.DataFrame(columns=dfHourDentro.columns)

            for ind in range(dfHourDentro_escalado.shape[0]):

                #Buscar si ya existe un registro en norm con esa fecha y hora 

                registroHour = dfHourDentro_escalado.iloc[ind]

                table_name = 'apicalidadaire_'+station+'_norm'

                query = f"SELECT * FROM {esquema}.{table_name} where date = '{registroHour.date}' and hour = {registroHour.hour}"

                print(query)

                dfnorm = pd.read_sql_query(query, engine)

                if not len(dfnorm)>0:

                    dfDatosNuevos = pd.concat([dfDatosNuevos,pd.DataFrame([registroHour])], ignore_index=True)

            dfDatosNuevos = dfDatosNuevos.applymap(lambda x: "nan" if pd.isna(x) else x)

            dfDatosNuevos = dfDatosNuevos.drop(columns=['idData'])

            dfDatosNuevos.to_sql(table_name, engine, if_exists='append', method='multi', index=False)


def InsertarDatosMerPROM():
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_traffic_MER_prom.csv')
    mer = pd.read_csv(ruta_csv)
    #mer = pd.read_csv('Datos/air_traffic_MER.csv')

    for ind in range(mer.shape[0]):
        
        #Query de insert
        query = f'INSERT INTO public."apicalidadaire_mer_prom_hr" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic) VALUES (\'{mer.loc[ind, "date"][0:10]}\',{mer.loc[ind, "CO"]},{mer.loc[ind, "NO"]},{mer.loc[ind, "NOX"]},{mer.loc[ind, "NO2"]},{mer.loc[ind, "O3"]},{mer.loc[ind, "PM10"]},{mer.loc[ind, "PM25"]},{mer.loc[ind, "RH"]},{mer.loc[ind, "SO2"]},{mer.loc[ind, "TMP"]},{mer.loc[ind, "WDR"]},{mer.loc[ind, "WSP"]},{mer.loc[ind, "year"]},{mer.loc[ind, "month"]},{mer.loc[ind, "day"]},{mer.loc[ind, "hour"]},{mer.loc[ind, "minute"]},{mer.loc[ind, "traffic"]});'
        
        query = query.replace("nan","\'nan\'")
        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def InsertarDatosUizPROM():
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_traffic_UIZ_prom.csv')
    uiz = pd.read_csv(ruta_csv)
    #uiz = pd.read_csv('Datos/air_and_traffic_UIZ.csv')

    for ind in range(uiz.shape[0]):

        #Query de insert
        query = f'INSERT INTO public."apicalidadaire_uiz_prom_hr" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic) VALUES (\'{uiz.loc[ind, "date"][0:10]}\',{uiz.loc[ind, "CO"]},{uiz.loc[ind, "NO"]},{uiz.loc[ind, "NOX"]},{uiz.loc[ind, "NO2"]},{uiz.loc[ind, "O3"]},{uiz.loc[ind, "PM10"]},{uiz.loc[ind, "PM25"]},{uiz.loc[ind, "RH"]},{uiz.loc[ind, "SO2"]},{uiz.loc[ind, "TMP"]},{uiz.loc[ind, "WDR"]},{uiz.loc[ind, "WSP"]},{uiz.loc[ind, "year"]},{uiz.loc[ind, "month"]},{uiz.loc[ind, "day"]},{uiz.loc[ind, "hour"]},{uiz.loc[ind, "minute"]},{uiz.loc[ind, "traffic"]});'

        query = query.replace("nan","\'nan\'")
        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()



def InsertarDatosMer15m():
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_traffic_MER_prom.csv')
    mer = pd.read_csv(ruta_csv)
    #mer = pd.read_csv('Datos/air_traffic_MER.csv')

    for ind in range(mer.shape[0]):
        
        #Query de insert
        query = f'INSERT INTO public."apicalidadaire_mer_15m" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic) VALUES (\'{mer.loc[ind, "date"][0:10]}\',{mer.loc[ind, "CO"]},{mer.loc[ind, "NO"]},{mer.loc[ind, "NOX"]},{mer.loc[ind, "NO2"]},{mer.loc[ind, "O3"]},{mer.loc[ind, "PM10"]},{mer.loc[ind, "PM25"]},{mer.loc[ind, "RH"]},{mer.loc[ind, "SO2"]},{mer.loc[ind, "TMP"]},{mer.loc[ind, "WDR"]},{mer.loc[ind, "WSP"]},{mer.loc[ind, "year"]},{mer.loc[ind, "month"]},{mer.loc[ind, "day"]},{mer.loc[ind, "hour"]},{mer.loc[ind, "minute"]},{mer.loc[ind, "traffic"]});'
        
        query = query.replace("nan","\'nan\'")
        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def InsertarDatosUiz15m():
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_traffic_UIZ_prom.csv')
    uiz = pd.read_csv(ruta_csv)
    #uiz = pd.read_csv('Datos/air_and_traffic_UIZ.csv')

    for ind in range(uiz.shape[0]):

        #Query de insert
        query = f'INSERT INTO public."apicalidadaire_uiz_15m" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic) VALUES (\'{uiz.loc[ind, "date"][0:10]}\',{uiz.loc[ind, "CO"]},{uiz.loc[ind, "NO"]},{uiz.loc[ind, "NOX"]},{uiz.loc[ind, "NO2"]},{uiz.loc[ind, "O3"]},{uiz.loc[ind, "PM10"]},{uiz.loc[ind, "PM25"]},{uiz.loc[ind, "RH"]},{uiz.loc[ind, "SO2"]},{uiz.loc[ind, "TMP"]},{uiz.loc[ind, "WDR"]},{uiz.loc[ind, "WSP"]},{uiz.loc[ind, "year"]},{uiz.loc[ind, "month"]},{uiz.loc[ind, "day"]},{uiz.loc[ind, "hour"]},{uiz.loc[ind, "minute"]},{uiz.loc[ind, "traffic"]});'

        query = query.replace("nan","\'nan\'")
        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

#InsertarDatosMer()
InsertarDatosUiz()

#InsertarDatosMerPROM()
InsertarDatosUizPROM()

#InsertarDatosMer15m()
InsertarDatosUiz15m()

#InsertarDatosEstaciones()

#InsertarDatosMerHr()

#InsertarDatosUizHr()

#NormDatosHr()
