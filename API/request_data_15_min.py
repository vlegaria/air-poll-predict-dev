import utils.utils
from utils.utils import *
from config.config import DATABASE_PASSWORD
import time
import psycopg2, psycopg2.extras
import pytz


#Ciclo que se ejecuta cada 15 min por siempre (o hasta que se interrumpe su ejecución)
stations2forecast = ['MER','UIZ']

while True:
    hora_actual = datetime.now(tz_mexico)
    hora = str(hora_actual.hour)
    minuto = str(hora_actual.minute)
    print(hora,":", minuto)
    
    if minuto == "0":
        try:
            print(hora,":", minuto)
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
    if minuto == "15":
        try:
            print(hora,":", minuto)
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
    if minuto == "30":
        try:
            print(hora,":", minuto)
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
    if minuto == "45":
        try:
            print(hora,":", minuto)
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
    
    if minuto == "55":
        #Funcion para calcular los promedios horarios
        try:
            get_hourly_averages(stations2forecast, hora_actual)
        except Exception as e:
            print("Ocurrió una excepción, no se pudieron calcular los promedios horarios:", e)

        #Función para normalizar los promedios horarios
        try:
            norm_data_averages(stations2forecast, hora_actual)
        except Exception as e:
            print("Ocurrio un problema al normalizar los promedios horarios, ", e)



    
            
    time.sleep(60)