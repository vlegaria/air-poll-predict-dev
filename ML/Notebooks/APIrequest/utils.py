import requests
import pandas as pd
from datetime import datetime
import locale
from config import TOMTOM_API_KEY, OPENWEATHER_API_KEY, DIR_REAL_TIME_DATA

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

  
def nearest_street_request(stations2forecast,printData):
    df_stations = pd.read_csv('estacionesCAMEcsv.csv')
    for station in stations2forecast:
        table = pd.read_csv(DIR_REAL_TIME_DATA)
        lat= df_stations.loc[df_stations['Key'] == station, 'Latitude'].values[0]
        lon= df_stations.loc[df_stations['Key'] == station, 'Longitude'].values[0]
        new_row = {}
        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
                url_tomtom = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/relative/16/json?point='+str(lat)+'%2C'+str(lon)+'&unit=KMPH&openLr=false&jsonp=jsonp&key='+ TOMTOM_API_KEY
                response = requests.get(url_tomtom)
                if response.status_code == 200:
                    data_tomtom = response.json()
                    if printData:
                        print(data_tomtom)
                    traffic_flow = data_tomtom.get('flowSegmentData').get('currentSpeed') / data_tomtom.get('flowSegmentData').get('freeFlowSpeed')
                    traffic_flow = "{:.6f}".format(traffic_flow)
                    new_row = {'TRAFFIC_FLOW' : traffic_flow}                    
                        #'frc': data_tomtom.get('flowSegmentData').get('frc'),
                        #'currentSpeed': data_tomtom.get('flowSegmentData').get('currentSpeed'),
                        #'freeFlowSpeed': data_tomtom.get('flowSegmentData').get('freeFlowSpeed'),
                        #'currentTravelTime': data_tomtom.get('flowSegmentData').get('currentTravelTime'),
                        #'freeFlowTravelTime': data_tomtom.get('flowSegmentData').get('freeFlowTravelTime'),
                        #'confidence': data_tomtom.get('flowSegmentData').get('confidence'),
                        #'roadClosure': data_tomtom.get('flowSegmentData').get('roadClosure'),
                    otro_intento = False
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API TomTom. Código de estado: {response.status_code}')

        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
                url_openweathermap = 'http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lat)+'&lon='+str(lon)+'&appid='+OPENWEATHER_API_KEY
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
                        'PM2_5': data_openweather.get('list')[0].get('components').get('pm2_5'),
                        'PM10': data_openweather.get('list')[0].get('components').get('pm10'),
                        }
                    otro_intento = False
                    new_row.update(new_row2)
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API OpenWeather. Código de estado: {response.status_code}')


        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
                url_openweathermap = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+OPENWEATHER_API_KEY
                new_row3 = {}
                response = requests.get(url_openweathermap)
                if response.status_code == 200:
                    data_openweather = response.json()
                    if printData:
                        print(data_openweather)
                    new_row3 = {
                        'TEMP': data_openweather.get('main').get('temp'),
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
            # Leer el archivo CSV existente            
            new_row_df = pd.DataFrame([new_row])
            # Añadir la nueva fila al DataFrame usando pd.concat
            df = pd.concat([table, new_row_df], ignore_index=True)                  
            # Escribir el DataFrame actualizado de nuevo al archivo CSV
            df.to_csv(DIR_REAL_TIME_DATA, index=False)
            print(station, "successful request")
    return



