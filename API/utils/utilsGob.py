from datetime import datetime
from config.config import TOMTOM_API_KEY, OPENWEATHER_API_KEY, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
from sqlalchemy import create_engine, text
import requests
import pandas as pd

datetime_now = datetime.now()
year = str(datetime_now.year)
date_df = datetime_now.strftime('%Y-%m-%d')
year = str(datetime_now.year)
month = str(datetime_now.month)
day = str(datetime_now.day)
hour = str(datetime_now.hour)

def nearest_street_request(stations2forecast,printData):

    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos de la ubicación de las estaciones y cargar en un DataFrame
    table_name = 'apicalidadaire_estacionescame'
    query = f"SELECT * FROM {esquema}.{table_name} where traffic = \'Si\';"
    print(query)
    df_stations = pd.read_sql_query(query, engine)

    #claveCont = ['nox','so2','co','nox','no2','no','o3','pm10','pm2','wsp','wdr','tmp','rh']
    claveCont = ['nox']

    #Crear dataframe vacio por estacion

    contEstacion = pd.DataFrame(columns=["station","date", "CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", "year", "month", "day", "hour", "minutes", "traffic"])

    for station in stations2forecast:
        contEstacion = pd.concat([contEstacion, {"station":station,
                                                 "date":datetime_now}])

    for cont in claveCont:
        urlGob = f"http://www.aire.cdmx.gob.mx/estadisticas-consultas/concentraciones/respuesta.php?qtipo=HORARIOS&parametro={cont}&anio={year}&qmes={month}"
        
        print(urlGob)
        df_consulta = pd.read_html(urlGob, encoding='windows-1252')

        df_datos = df_consulta[0]

        df_datos.columns = df_datos.iloc[1]

        df_datos = df_datos.drop([0,1])

        print(df_datos.head())

    return
