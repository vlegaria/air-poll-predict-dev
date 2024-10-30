import requests
import pandas as pd
from datetime import datetime, date
import locale
from config.config import TOMTOM_API_KEY, OPENWEATHER_API_KEY, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
import os
from sqlalchemy import create_engine, text
import psycopg2
import pickle
from sklearn.preprocessing import MinMaxScaler
import numpy as np
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
                    TRFC = traffic_flow
                    otro_intento = False
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API TomTom. Código de estado: {response.status_code}')

        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
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
                    otro_intento = False
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
                    TMP =data_openweather.get('main').get('temp')
                    RH= data_openweather.get('main').get('humidity')
                    WSP = data_openweather.get('wind').get('speed')
                    WDR= data_openweather.get('wind').get('deg')
                    otro_intento = False
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API OpenWeather. Código de estado: {response.status_code}')

        columnas = ["date", "CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", "year", "month", "day", "hour", "minutes", "traffic"]
        datetime_now = datetime.now()
        date_df = datetime_now.strftime('%Y-%m-%d')
        year= str(datetime_now.year)
        month= str(datetime_now.month)
        day = str(datetime_now.day)
        hour = str(datetime_now.hour)
        minute= str(datetime_now.minute)
        values = [date_df, CO, NO, 0, NO2, O3, PM10, PM25, RH, SO2, TMP, WDR, WSP, year, month, day, hour, minute,TRFC]

        print(station, "successful request")


        df = pd.DataFrame([values], columns=columnas)
        engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        table_name = 'apicalidadaire_'+station.lower()+'_15m'
        # Insertar datos en la tabla de PostgreSQL
        df.to_sql(table_name, engine, if_exists='append', index=False)
    return

def get_hourly_averages(stations2forecast, timenow): 
    for station in stations2forecast:
        engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        esquema = 'public'
        # Recuperar los datos de la hora y cargar en un DataFrame
        table_name = 'apicalidadaire_'+station+'_15m'
        query = f"SELECT * FROM {esquema}.{table_name} WHERE date = '{timenow.year}-{timenow.month}-{timenow.day}' and hour = {timenow.hour};"
        print(query)
        df = pd.read_sql_query(query, engine)

        if len(df)>0:
            tableProm1h = f"apicalidadaire_{station}_prom_hr"

            #Si son negativos o vacios cambiarlos a nan
            for ind in range(df.shape[0]):
                for dato in df.columns:
                    if(dato in ["CO", "NO",  "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", "traffic"]):
                        if(df.loc[ind, dato] < 0):
                            df.loc[ind, dato] = np.nan
                          
                        if(df.loc[ind, dato] == ""):
                            df.loc[ind, dato] = np.nan
        
                #Query para insertar los promedios 
            queryInsert = f"""INSERT INTO {esquema}.{tableProm1h}( date, \"CO\", \"NO\", \"NOX\", \"NO2\", \"O3\", \"PM10\", \"PM25\", \"RH\", \"SO2\", \"TMP\", \"WDR\", \"WSP\", year, month, day, hour, minutes, traffic) VALUES 
            (\'{timenow.year}-{timenow.month}-{timenow.day}\', {df["CO"].mean()}, {df["NO"].mean()}, {df["NOX"].mean()}, {df["NO2"].mean()}, {df["O3"].mean()}, {df["PM10"].mean()}, {df["PM25"].mean()}, {df["RH"].mean()}, 
            {df["SO2"].mean()}, {df["TMP"].mean()}, {df["WDR"].mean()}, {df["WSP"].mean()}, {timenow.year}, {timenow.month}, {timenow.day}, {timenow.hour}, 0, {df["traffic"].mean()});"""

            print(queryInsert)

            #ejecutamos insert
            with engine.connect() as conn:
                conn.execute(text(queryInsert))
                conn.commit()


    return 


def norm_data_averages(stations2forecast, timenow):
    for station in stations2forecast:
        engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        esquema = 'public'
        # Recuperar los datos de la hora y cargar en un DataFrame
        table_name = 'apicalidadaire_'+station+'_prom_hr'
        query = f"SELECT * FROM {esquema}.{table_name} WHERE date = '{timenow.year}-{timenow.month}-{timenow.day}' and hour = {timenow.hour};"
        print(query)
        df = pd.read_sql_query(query, engine)

        if len(df)>0:

            #Ejecutando desde carpeta raiz air-poll-predict-dev
            with open(f'ML/Scalers/{station}_scaler.pkl', "rb") as f:
                scaler = pickle.load(f)

            #Tomar los escalers de mlflow por parametros


            df_escalado = df.copy()

            df_escalado[["CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]] = scaler.transform(df[["CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]])

            reescalar_Data = False

            #Verificar que los datos escalados se encuentren dentro del minimo y maximo establecido 
            for dato in df_escalado.columns:
                if(dato in ["CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]):
                    if(df_escalado.loc[0, dato] < 0 or df_escalado.loc[0, dato] >  1):
                        reescalar_Data = True
                        print(df_escalado.loc[0, dato])

            if(reescalar_Data):

                # Recuperar los datos de la hora y cargar en un DataFrame
                table_name = 'apicalidadaire_'+station+'_norm'
                query = f"SELECT * FROM {esquema}.{table_name};"
                print(query)
                df_norm = pd.read_sql_query(query, engine)

                df_data = df_norm.copy()
                
                for index, row in df_norm.iterrows():
                    # Seleccionamos los valores de la fila y los transformamos a un array de 1x12
                    row_values = row[["CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]].values.reshape(1, -1)
                    
                    # Aplicamos inverse_transform y convertimos el resultado en un array plano
                    inverse_values = scaler.inverse_transform(row_values).flatten()
                    
                    # Asignamos los valores transformados a las columnas correspondientes
                    df_data.loc[index, ["CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]] = inverse_values
                    #print(nuevaRow)

                #Agregamos valor de ultima consulta hora
                df_data = pd.concat([df_data, df], ignore_index=True)

                nuevoScaler = MinMaxScaler()

                #Obtenemos los nuevos escalers
                nuevoScaler.fit(df_data[["CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]])

                df_norm_data_escalada = df_data.copy()

                #Obtener los nuevos valores escalados
                df_norm_data_escalada[["CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]] = nuevoScaler.transform(df_data[["CO", "NO", "NOX", "NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP"]])

                #Limpiar tabla para insertar nuevos valores escalados
                query = f"DELETE FROM {esquema}.{table_name};"
                print(query)
                with engine.connect() as conn:
                    conn.execute(text(query))
                    conn.commit()

                #Insertar nuevos valores normalizados con la nueva escala en la base de datos
                for indNorm in range(df_norm_data_escalada.shape[0]):

                    queryInsert = f"""INSERT INTO {esquema}.{table_name}( date, \"CO\", \"NO\", \"NOX\", \"NO2\", \"O3\", \"PM10\", \"PM25\", \"RH\", \"SO2\", \"TMP\", \"WDR\", \"WSP\", year, month, day, hour, minutes, traffic) VALUES 
                    (\'{df_norm_data_escalada.loc[indNorm,"date"]}\', {df_norm_data_escalada.loc[indNorm,"CO"]}, {df_norm_data_escalada.loc[indNorm,"NO"]}, {df_norm_data_escalada.loc[indNorm,"NOX"]}, {df_norm_data_escalada.loc[indNorm,"NO2"]}, {df_norm_data_escalada.loc[indNorm,"O3"]}, {df_norm_data_escalada.loc[indNorm,"PM10"]}, {df_norm_data_escalada.loc[indNorm,"PM25"]}, {df_norm_data_escalada.loc[indNorm,"RH"]}, 
                    {df_norm_data_escalada.loc[indNorm,"SO2"]}, {df_norm_data_escalada.loc[indNorm,"TMP"]}, {df_norm_data_escalada.loc[indNorm,"WDR"]}, {df_norm_data_escalada.loc[indNorm,"WSP"]}, {df_norm_data_escalada.loc[indNorm,"year"]}, {df_norm_data_escalada.loc[indNorm,"month"]}, {df_norm_data_escalada.loc[indNorm,"day"]}, {df_norm_data_escalada.loc[indNorm,"hour"]}, 0, {df_norm_data_escalada.loc[indNorm,"traffic"]});"""

                    #print(queryInsert)

                    #ejecutamos insert
                    with engine.connect() as conn:
                        conn.execute(text(queryInsert))
                        conn.commit()

                #Exportar pkl con nuevo escaler
                pickle.dump(nuevoScaler, open(f'ML/Scalers/{station}_scaler.pkl', "wb"))

                #Rentrenar modelos, subirlos a mlflow


            else:
                print("Insertar nuevo normalizado")
                #Query para insertar los valores normalizados 
                queryInsert = f"""INSERT INTO {esquema}.{table_name}( date, \"CO\", \"NO\", \"NOX\", \"NO2\", \"O3\", \"PM10\", \"PM25\", \"RH\", \"SO2\", \"TMP\", \"WDR\", \"WSP\", year, month, day, hour, minutes, traffic) VALUES 
                (\'{timenow.year}-{timenow.month}-{timenow.day}\', {df_escalado.loc[0,"CO"]}, {df_escalado.loc[0,"NO"]}, {df_escalado.loc[0,"NOX"]}, {df_escalado.loc[0,"NO2"]}, {df_escalado.loc[0,"O3"]}, {df_escalado.loc[0,"PM10"]}, {df_escalado.loc[0,"PM25"]}, {df_escalado.loc[0,"RH"]}, 
                {df_escalado.loc[0,"SO2"]}, {df_escalado.loc[0,"TMP"]}, {df_escalado.loc[0,"WDR"]}, {df_escalado.loc[0,"WSP"]}, {timenow.year}, {timenow.month}, {timenow.day}, {timenow.hour}, 0, {df_escalado.loc[0,"traffic"]});"""

                print(queryInsert)

                #ejecutamos insert
                with engine.connect() as conn:
                    conn.execute(text(queryInsert))
                    conn.commit()
                




        

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
