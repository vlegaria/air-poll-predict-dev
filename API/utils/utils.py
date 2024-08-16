import requests
import pandas as pd
from datetime import datetime
import locale
from config.config import TOMTOM_API_KEY, OPENWEATHER_API_KEY, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
import os
from sqlalchemy import create_engine
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


def nearest_street_request(stations2forecast,printData):
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    esquema = 'public'
    # Recuperar los datos de la ubicación de las estaciones y cargar en un DataFrame
    table_name = 'apicalidadaire_estacionescame'
    query = f"SELECT * FROM {esquema}.{table_name};"
    df_stations = pd.read_sql_query(query, engine)
    df_stations = df_stations.loc[df_stations['traffic'] == 'Si']
    for station in stations2forecast:
        lat= df_stations.loc[df_stations['key'] == station, 'latitude'].values[0]
        lon= df_stations.loc[df_stations['key'] == station, 'longitude'].values[0]
        otro_intento1 = True
        for intentos in range(3):
            if otro_intento1 ==True:
                url_tomtom = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/relative/16/json?point='+str(lat)+'%2C'+str(lon)+'&unit=KMPH&openLr=false&jsonp=jsonp&key='+TOMTOM_API_KEY
                response = requests.get(url_tomtom)
                if response.status_code == 200:
                    data_tomtom = response.json()
                    if printData:
                        print(data_tomtom)
                    traffic_flow = data_tomtom.get('flowSegmentData').get('currentSpeed') / data_tomtom.get('flowSegmentData').get('freeFlowSpeed')
                    traffic_flow = "{:.6f}".format(traffic_flow)
                    TRFC = traffic_flow
                    otro_intento1 = False
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API TomTom. Código de estado: {response.status_code}')

        otro_intento2 = True
        for intentos in range(3):
            if otro_intento2 ==True:
                url_openweathermap = 'http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lat)+'&lon='+str(lon)+'&appid='+ OPENWEATHER_API_KEY
                response = requests.get(url_openweathermap)
                if response.status_code == 200:
                    data_openweather = response.json()
                    if printData:
                        print(data_openweather)
                        CO= data_openweather.get('list')[0].get('components').get('co')
                        NO= data_openweather.get('list')[0].get('components').get('no')
                        NO2= data_openweather.get('list')[0].get('components').get('no2')
                        O3= data_openweather.get('list')[0].get('components').get('o3')
                        SO2= data_openweather.get('list')[0].get('components').get('so2')
                        PM25= data_openweather.get('list')[0].get('components').get('pm2_5')
                        PM10= data_openweather.get('list')[0].get('components').get('pm10')
                    otro_intento2 = False
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API OpenWeather. Código de estado: {response.status_code}')

        otro_intento3 = True
        for intentos in range(3):
            if otro_intento3 ==True:
                url_openweathermap = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+ OPENWEATHER_API_KEY
                new_row3 = {}
                response = requests.get(url_openweathermap)
                if response.status_code == 200:
                    data_openweather = response.json()
                    if printData:
                        print(data_openweather)
                        TMP =data_openweather.get('main').get('temp')
                        RH= data_openweather.get('main').get('humidity')
                        WSP = data_openweather.get('wind').get('speed')
                        WDR= data_openweather.get('wind').get('deg')
                    otro_intento3 = False
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API OpenWeather. Código de estado: {response.status_code}')

    columnas = ["date", "CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", "year", "month", "day", "hour", "minutes", "traffic"]
    datetime_now = datetime.now()
    date = datetime_now.strftime('%Y-%m-%d')
    year= str(datetime_now.year)
    month= str(datetime_now.month)
    day = str(datetime_now.day)
    hour = str(datetime_now.hour)
    minute= str(datetime_now.minute)
    values = [date, CO, NO, 0, NO2, O3, PM10, PM25, RH, SO2, TMP, WDR, WSP, year, month, day, hour, minute,TRFC]

    if otro_intento1 == False and otro_intento2 == False and otro_intento3 == False:
        if printData:
            print(station, "successful request")
        df = pd.DataFrame([values], columns=columnas)
        engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        table_name = 'apicalidadaire_'+station.lower()+'_15m'
        # Insertar datos en la tabla de PostgreSQL
        df.to_sql(table_name, engine, if_exists='append', index=False)

    return

def get_hourly_averages(stations2forecast):
    for station in stations2forecast:
        engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        esquema = 'public'
        # Recuperar los datos y cargar en un DataFrame
        table_name = 'apicalidadaire_'+station+'_m'
        query = f"SELECT * FROM {esquema}.{table_name};"
        df = pd.read_sql_query(query, engine)
        df['datetime'] = pd.to_datetime(
                df['date'] + ' ' + df['timestamp'],
                format='%d/%m/%Y %H:%M:%S',
                dayfirst=True,
                errors='coerce'
            )
        # Redondear las fechas a la hora más cercana
        df['date'] = df['datetime'].dt.round('H')
        # Agrupar por la hora redondeada y calcular el promedio de las mediciones
        df_new = df.groupby('date').agg({
            'CO': 'mean',  # Calcular el promedio de las mediciones  
            'NO': 'mean', 
            'NO2': 'mean',  
            'PM10': 'mean',  
            'PM25': 'mean',  
            'SO2': 'mean',  
            'O3': 'mean',  
            'TMP': 'mean',
            'RH': 'mean',  
            'WSP': 'mean',
            'WDR': 'mean',  
            'TRAFFIC_FLOW': 'mean'
        }).reset_index()

        df_new['year'] = df_new['date'].dt.year
        df_new['month'] = df_new['date'].dt.month
        df_new['day'] = df_new['date'].dt.day
        df_new['hour'] = df_new['date'].dt.hour
        df_new['minute'] = df_new['date'].dt.minute
        
        # Crear el motor de conexión a la base de datos
        engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        table_name = 'apicalidadaire_'+station+'_norm'
        # Insertar datos en la tabla de PostgreSQL
        df_new.to_sql(table_name, engine, if_exists='append', index=False)
    return 


def consult_tables():
    # Conectar a la base de datos
    try:
        connection = psycopg2.connect(
            host = DATABASE_HOST,
            dbname = DATABASE_NAME,
            user = DATABASE_USER,
            password = DATABASE_PASSWORD
        )
        cursor = connection.cursor()


        # Ejecutar una consulta para obtener las tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)

        # Obtener los resultados
        tables = cursor.fetchall()

        # Mostrar las tablas disponibles
        print("Tablas en la base de datos:")
        for table in tables:
            print(table[0])

    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)

    finally:
        # Cerrar la conexión
        if connection:
            cursor.close()
            connection.close()

    return
