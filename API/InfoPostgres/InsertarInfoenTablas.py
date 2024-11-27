from config.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np
import os

#Conexión a la base de datos

engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
esquema = 'public'
table_name = 'apicalidadaire_prediccion'

#Insertar datos de Mer_Norm


def InsertarDatosMer():
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_traffic_MER.csv')
    mer = pd.read_csv(ruta_csv)
    #mer = pd.read_csv('Datos/air_traffic_MER.csv')

    for ind in range(mer.shape[0]):
        
        #Query de insert
        query = f'INSERT INTO public."apicalidadaire_mer_norm" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic) VALUES (\'{mer.loc[ind, "date"][0:10]}\',{mer.loc[ind, "CO"]},{mer.loc[ind, "NO"]},{mer.loc[ind, "NOX"]},{mer.loc[ind, "NO2"]},{mer.loc[ind, "O3"]},{mer.loc[ind, "PM10"]},{mer.loc[ind, "PM25"]},{mer.loc[ind, "RH"]},{mer.loc[ind, "SO2"]},{mer.loc[ind, "TMP"]},{mer.loc[ind, "WDR"]},{mer.loc[ind, "WSP"]},{mer.loc[ind, "year"]},{mer.loc[ind, "month"]},{mer.loc[ind, "day"]},{mer.loc[ind, "hour"]},{mer.loc[ind, "minute"]},{mer.loc[ind, "traffic"]});'
        
        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def InsertarDatosUiz():
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_actual, 'Datos', 'air_and_traffic_UIZ.csv')
    uiz = pd.read_csv(ruta_csv)
    #uiz = pd.read_csv('Datos/air_and_traffic_UIZ.csv')

    for ind in range(uiz.shape[0]):

        #Query de insert
        query = f'INSERT INTO public."apicalidadaire_uiz_norm" ("date", "CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", year, month, day, hour, minutes, traffic) VALUES (\'{uiz.loc[ind, "date"][0:10]}\',{uiz.loc[ind, "CO"]},{uiz.loc[ind, "NO"]},{uiz.loc[ind, "NOX"]},{uiz.loc[ind, "NO2"]},{uiz.loc[ind, "O3"]},{uiz.loc[ind, "PM10"]},{uiz.loc[ind, "PM25"]},{uiz.loc[ind, "RH"]},{uiz.loc[ind, "SO2"]},{uiz.loc[ind, "TMP"]},{uiz.loc[ind, "WDR"]},{uiz.loc[ind, "WSP"]},{uiz.loc[ind, "year"]},{uiz.loc[ind, "month"]},{uiz.loc[ind, "day"]},{uiz.loc[ind, "hour"]},{uiz.loc[ind, "minute"]},{uiz.loc[ind, "traffic"]});'

        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

def InsertarDatosEstaciones():
    estaciones = pd.read_csv('Datos/estacionesCAME.csv')

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

InsertarDatosMer()
#InsertarDatosUiz()

#InsertarDatosEstaciones()
