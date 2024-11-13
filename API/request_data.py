import time
import requests

from utils.utilsGob import *
from utils.utils import *


stations2forecast = ['MER','UIZ']

urlGob = "http://www.aire.cdmx.gob.mx/estadisticas-consultas/concentraciones/index.php"

while True:

    hora_actual = datetime.now()
    hora = str(hora_actual.hour)
    minuto = str(hora_actual.minute)
    print(hora,":", minuto)

    if int(minuto) % 15 == 0  and int(minuto) != 60:

        try:
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
            

    
    if int(minuto) == 55:

        #Verificamos si la pagina del gobierno esta caida y si es asi consultamos en Api
        response = requests.get(urlGob)

        if response.status_code == 200:
            try:
                nearest_street_requestGob(stations2forecast, printData=False)
            except Exception as e:
                print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)

        else:
            try:
                get_hourly_averages(stations2forecast, hora_actual)
            except Exception as e:
                print("Ocurrió una excepción, no se pudieron calcular los promedios horarios:", e)

        try:
            norm_data_averages(stations2forecast, hora_actual)
        except Exception as e:
            print("Ocurrio un problema al normalizar los promedios horarios, ", e)

    time.sleep(60)
            