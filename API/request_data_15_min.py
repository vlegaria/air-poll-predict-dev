import utils.utils
from utils.utils import *
from config.config import DATABASE_PASSWORD
import time
import psycopg2, psycopg2.extras

#Ciclo que se ejecuta cada 15 min por siempre (o hasta que se interrumpe su ejecución)
stations2forecast = ['MER', 'UIZ']
while True:
    hora_actual = datetime.now()
    hora = str(hora_actual.hour)
    minuto = str(hora_actual.minute)
    print(hora,":", minuto)
    if minuto == "5":
        try:
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
        #Funcion para calcular los promedios horarios
        try:
            get_hourly_averages(stations2forecast, hora_actual)
        except Exception as e:
            print("Ocurrió una excepción, no se pudieron calcular los promedios horarios:", e)
    if minuto == "15":
        try:
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
    if minuto == "30":
        try:
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
    if minuto == "45":
        try:
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)

            
    time.sleep(60)