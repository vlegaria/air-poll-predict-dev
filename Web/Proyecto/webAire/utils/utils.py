import requests
import pandas as pd
from datetime import datetime
import locale
from config.config import TOMTOM_API_KEY, OPENWEATHER_API_KEY, DATABASE_PASSWORD, DATABASE_USER, DATABASE_HOST, DATABASE_NAME
import os
import psycopg2
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


def nearest_street_request(stations2forecast,printData):
    df_stations = pd.read_csv('estacionesCAMEcsv.csv')
    for station in stations2forecast:
        lat= df_stations.loc[df_stations['Key'] == station, 'Latitude'].values[0]
        lon= df_stations.loc[df_stations['Key'] == station, 'Longitude'].values[0]
        new_row = {}
        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
                url_tomtom = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/relative/16/json?point='+str(lat)+'%2C'+str(lon)+'&unit=KMPH&openLr=false&jsonp=jsonp&key='+TOMTOM_API_KEY
                response = requests.get(url_tomtom)
                if response.status_code == 200:
                    data_tomtom = response.json()
                    if printData:
                        print(data_tomtom)
                    traffic_flow = data_tomtom.get('flowSegmentData').get('currentSpeed') / data_tomtom.get('flowSegmentData').get('freeFlowSpeed')
                    traffic_flow = "{:.6f}".format(traffic_flow)
                    new_row = {'TRAFFIC_FLOW' : traffic_flow}                    
                    otro_intento = False
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API TomTom. Código de estado: {response.status_code}')

        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
                url_openweathermap = 'http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lat)+'&lon='+str(lon)+'&appid='+ OPENWEATHER_API_KEY
                new_row2 = {}
                response = requests.get(url_openweathermap)
                if response.status_code == 200:
                    data_openweather = response.json()
                    if printData:
                        print(data_openweather)
                    new_row2 = {
                        'CO': data_openweather.get('list')[0].get('components').get('co'),
                        'NO': data_openweather.get('list')[0].get('components').get('no'),
                        'NO2': data_openweather.get('list')[0].get('components').get('no2'),
                        'O3': data_openweather.get('list')[0].get('components').get('o3'),
                        'SO2': data_openweather.get('list')[0].get('components').get('so2'),
                        'PM25': data_openweather.get('list')[0].get('components').get('pm2_5'),
                        'PM10': data_openweather.get('list')[0].get('components').get('pm10'),
                        }
                    otro_intento = False
                    new_row.update(new_row2)
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API OpenWeather. Código de estado: {response.status_code}')


        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
                url_openweathermap = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+ OPENWEATHER_API_KEY
                new_row3 = {}
                response = requests.get(url_openweathermap)
                if response.status_code == 200:
                    data_openweather = response.json()
                    if printData:
                        print(data_openweather)
                    new_row3 = {
                        'TMP': data_openweather.get('main').get('temp'),
                        'RH': data_openweather.get('main').get('humidity'),
                        'WSP': data_openweather.get('wind').get('speed'),
                        'WDR': data_openweather.get('wind').get('deg'),
                        }
                    otro_intento = False
                    new_row.update(new_row3)
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API OpenWeather. Código de estado: {response.status_code}')

        if len(new_row) != 0:
            new_row["STATION"] = station
            datetime_now = datetime.now()
            date = datetime_now.strftime('%Y-%m-%d')
            timestamp = datetime_now.strftime('%H:%M:%S')
            hour = str(datetime_now.hour)
            minute= str(datetime_now.minute)
            new_row['date'] = date
            new_row['timestamp'] = timestamp
            new_row['hour'] = hour
            new_row['minute'] = minute
            print(station, "successful request")
    return new_row

def get_hourly_averages():
    # Conectar a la base de datos
    try:
        """
        connection = psycopg2.connect(
            host = DATABASE_HOST,
            dbname = DATABASE_NAME,
            user = DATABASE_USER,
            password = DATABASE_PASSWORD
        )
        cursor = connection.cursor()
        tables = ["apiCalidadAire_mer_norm", "apiCalidadAire_ped_norm", "apiCalidadAire_uiz_norm"]
        for table in tables:
        # Ejecutar una consulta
        cursor.execute("SELECT * FROM apiCalidadAire_mer_norm")
        # Obtener los resultados
        rows = cursor.fetchall()
        # Procesar los resultados
        for row in rows:
            print(row)
        """
        dir = 'C:/Users/valer/Desktop/DataStations/traffic_and_airvisual.csv'
        df = pd.read_csv(dir)
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
        print(df_new)
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)

    finally:
        """
        # Cerrar la conexión
        if connection:
            cursor.close()
            connection.close()
        """
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