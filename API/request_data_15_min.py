import utils.utils
from utils.utils import *
from config.config import DATABASE_PASSWORD
import time
import psycopg2, psycopg2.extras
import pytz

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
tz_mexico = pytz.timezone('America/Mexico_City')
#Ciclo que se ejecuta cada 15 min por siempre (o hasta que se interrumpe su ejecución)
stations2forecast = ['MER', 'UIZ']
hora_actual = datetime.now(tz_mexico)
hora = str(hora_actual.hour)
minuto = str(hora_actual.minute)
print(hora,":", minuto)
while True:
    hora_actual = datetime.now(tz_mexico)
    hora = str(hora_actual.hour)
    minuto = str(hora_actual.minute)
    #print(hora,":", minuto)
    if minuto == "5":
        try:
            print(hora,":", minuto)
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
        #Funcion para calcular los promedios horarios
        try:
            get_hourly_averages(stations2forecast, hora_actual)
        except Exception as e:
            print("Ocurrió una excepción, no se pudieron calcular los promedios horarios:", e)
        #Funcion para calcular los promedios horarios
        try:
            normalization(stations2forecast, hora_actual)
        except Exception as e:
            print("Ocurrió una excepción, no se pudo realizar la normalizacion:", e)            
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

            
    time.sleep(60)