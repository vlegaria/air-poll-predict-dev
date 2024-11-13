from datetime import datetime
from config.config import TOMTOM_API_KEY, OPENWEATHER_API_KEY, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
from sqlalchemy import create_engine, text
import requests
import pandas as pd
import numpy as np



#Datos bbdd
engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
esquema = 'public'

def nearest_street_requestGob(stations2forecast,printData):

    datetime_now = datetime.now()
    year = str(datetime_now.year)
    date_df = datetime_now.strftime('%Y-%m-%d')
    year = str(datetime_now.year)
    month = str(datetime_now.month)
    day = str(datetime_now.day)
    hour = str(datetime_now.hour)
    minute= str(datetime_now.minute)

    #Preparar datos para buscar tabla
    dayText = f'0{day}' if len(str(day)) == 1 else str(day)
    monthText = f'0{month}' if len(str(month))  == 1 else str(month)
    dateData = f'{dayText}-{monthText}-{year}'
    
    claveCont = ['nox','so2','co','nox','no2','no','o3','pm10','pm2','wsp','wdr','tmp','rh']

    #Crear dataframe vacio por estacion

    contEstacion = pd.DataFrame(columns=["station","date", "CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", "year", "month", "day", "hour", "minutes", "traffic"])

    for station in stations2forecast:
        contEstacion = pd.concat([contEstacion, pd.DataFrame({"station":station,
                                                 "date":datetime_now,
                                                 "year":year,
                                                 "month":month,
                                                 "day":day,
                                                 "hour":hour,
                                                 "minutes":"0"}, index=[0])], ignore_index=True)
 
    #print(contEstacion.head())

    for cont in claveCont:
        urlGob = f"http://www.aire.cdmx.gob.mx/estadisticas-consultas/concentraciones/respuesta.php?qtipo=HORARIOS&parametro={cont}&anio={year}&qmes={month}"
        
        #print(urlGob)
        df_consulta = pd.read_html(urlGob, encoding='windows-1252')

        df_datos = df_consulta[0]

        df_datos.columns = df_datos.iloc[1]

        df_datos = df_datos.drop([0,1])

        #print(df_datos.head())

        #Nombre de la culmna del contaminante en el dataframe de estaciones
        if(cont == "pm2"):
            colEstation = "PM25"
        else: 
            colEstation = cont.upper()


        for station in stations2forecast:
            dataofDay = df_datos.loc[df_datos['Fecha'] == dateData, ["Hora",station]]

            dato = dataofDay.loc[dataofDay['Hora'] == hour, station].values[0]

            if(dato != "nr"):
                if float(dato) >= 0:
                    contEstacion.loc[contEstacion['station'] == station, colEstation] = dato
                else: 
                    contEstacion.loc[contEstacion['station'] == station, colEstation] = np.nan
            else: 
                contEstacion.loc[contEstacion['station'] == station, colEstation] = np.nan

    

    #Obtener trafico de Api

    for station in stations2forecast:

        #Obtenemos los valores de trafico y los promediamos
        table_name = 'apicalidadaire_'+station+'_15m'
        query = f"SELECT * FROM {esquema}.{table_name} WHERE date = '{year}-{month}-{day}' and hour = {hour};"
        print(query)
        df_traffic = pd.read_sql_query(query, engine)
        
        contEstacion.loc[contEstacion['station'] == station, "traffic"] = df_traffic["traffic"].mean()

        tableProm1h = f"apicalidadaire_{station.lower()}_prom_hr"

        queryInsert = f"""INSERT INTO {esquema}.{tableProm1h}( date, \"CO\", \"NO\", \"NOX\", \"NO2\", \"O3\", \"PM10\", \"PM25\", \"RH\", \"SO2\", \"TMP\", \"WDR\", \"WSP\", year, month, day, hour, minutes, traffic) VALUES 
            (\'{datetime_now}\', {contEstacion.loc[contEstacion['station'] == station,"CO"].values[0]}, {contEstacion.loc[contEstacion['station'] == station,"NO"].values[0]}, {contEstacion.loc[contEstacion['station'] == station,"NOX"].values[0]}, 
            {contEstacion.loc[contEstacion['station'] == station,"NO2"].values[0]}, {contEstacion.loc[contEstacion['station'] == station,"O3"].values[0]}, {contEstacion.loc[contEstacion['station'] == station,"PM10"].values[0]}, {contEstacion.loc[contEstacion['station'] == station,"PM25"].values[0]}, 
            {contEstacion.loc[contEstacion['station'] == station,"RH"].values[0]}, {contEstacion.loc[contEstacion['station'] == station,"SO2"].values[0]}, {contEstacion.loc[contEstacion['station'] == station,"TMP"].values[0]}, {contEstacion.loc[contEstacion['station'] == station,"WDR"].values[0]}, 
            {contEstacion.loc[contEstacion['station'] == station,"WSP"].values[0]}, {year}, {month}, {day}, {hour}, 0, {contEstacion.loc[contEstacion['station'] == station,"traffic"].values[0]});"""

        #Dar formato a los nan para insertar en tabla
        queryInsert = queryInsert.replace("nan","\'nan\'")

        print(queryInsert)

        #ejecutamos insert
        with engine.connect() as conn:
            conn.execute(text(queryInsert))
            conn.commit()
    

    return


def request_traffic(stations2forecast, printData):
    datetime_now = datetime.now()
    year = str(datetime_now.year)
    date_df = datetime_now.strftime('%Y-%m-%d')
    year = str(datetime_now.year)
    month = str(datetime_now.month)
    day = str(datetime_now.day)
    hour = str(datetime_now.hour)
    minute= str(datetime_now.minute)

    # Recuperar los datos de la ubicación de las estaciones y cargar en un DataFrame
    table_name = 'apicalidadaire_estacionescame'
    query = f"SELECT * FROM {esquema}.{table_name} where traffic = \'Si\';"
    #print(query)
    df_stations = pd.read_sql_query(query, engine)

    for station in stations2forecast:

        if(len(df_stations.loc[df_stations['key'] == station, 'latitude']) > 0):
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
            
            columnas = ["date", "CO", "NO", "NOX","NO2", "O3", "PM10", "PM25", "RH", "SO2", "TMP", "WDR", "WSP", "year", "month", "day", "hour", "minutes", "traffic"]
            values = [date_df, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, year, month, day, hour, minute,TRFC]

            df = pd.DataFrame([values], columns=columnas)
            table_name = 'apicalidadaire_'+station.lower()+'_15m'
            # Insertar datos en la tabla de PostgreSQL
            df.to_sql(table_name, engine, if_exists='append', index=False)

    return


