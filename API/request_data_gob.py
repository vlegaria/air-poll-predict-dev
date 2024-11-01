import time

from utils.utilsGob import *
from utils.utils import *

stations2forecast = ['MER','UIZ']

#Ciclo para adquirir datos cada hora de pagina de gobierno

while True:
    hora_actual = datetime.now()
    hora = str(hora_actual.hour)
    minuto = str(hora_actual.minute)
    print(hora,":", minuto)

    if int(minuto) % 15 == 0  and int(minuto) != 60:
        print("Obtener trafico")
        try:
            request_traffic(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)

    
    if int(minuto) == 55:
        try:
            nearest_street_requestGob(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)

        try:
            norm_data_averages(stations2forecast, hora_actual)
        except Exception as e:
            print("Ocurrio un problema al normalizar los promedios horarios, ", e)
            
    time.sleep(60)