import time
from datetime import datetime
from utils_TomTom import *

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def main():
    stations2forecast = ['MER']
    while True:
        hora_actual = datetime.now()
        hora = str(hora_actual.hour)
        minuto = str(hora_actual.minute)
        print(hora,":", minuto)
        if minuto == "0":
            try:
                nearest_street_request(stations2forecast)
            except Exception as e:
                print("No se descargaron datos a las: ", hora,":", minuto)
                print("Ocurrió una excepción:", e)
        if minuto == "15":
            try:
                nearest_street_request(stations2forecast)
            except Exception as e:
                print("No se descargaron datos a las: ", hora,":", minuto)
                print("Ocurrió una excepción:", e)
        if minuto == "30":
            try:
                nearest_street_request(stations2forecast)
            except Exception as e:
                print("No se descargaron datos a las: ", hora,":", minuto)
                print("Ocurrió una excepción:", e)
        if minuto == "45":
            try:
                nearest_street_request(stations2forecast)
            except Exception as e:
                print("No se descargaron datos a las: ", hora,":", minuto)
                print("Ocurrió una excepción:", e)

        time.sleep(60)


if __name__ == "__main__":
    main()
