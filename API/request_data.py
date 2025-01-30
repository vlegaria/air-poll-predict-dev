import time
import requests

from utils.utilsGob import *
from utils.utils import *

import subprocess


stations2forecast = ['MER','UIZ']

urlGob = "http://www.aire.cdmx.gob.mx/estadisticas-consultas/concentraciones/index.php"

deltaDias = timedelta(days = 7)

fechaUltimoEnt = date.today()

fechaConsulta = fechaUltimoEnt + deltaDias


locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
tz_mexico = pytz.timezone('America/Mexico_City')
while True:

    hora_actual = datetime.now(tz_mexico)
    hora = str(hora_actual.hour)
    minuto = str(hora_actual.minute)
    print(hora,":", minuto)

    fecha_actual = date.today()

    if int(minuto) % 15 == 0  and int(minuto) != 60:
        try:
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)
            

    
    if int(minuto) == 24:

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

        #try:
        #    norm_data_averages(stations2forecast, hora_actual)
        #except Exception as e:
        #    print("Ocurrio un problema al normalizar los promedios horarios, ", e)
        #subprocess.Popen(['../../Webaire/Scripts/python.exe', 'norm_data.py']) #Se pone la ubicación de python.exe del Env, en caso que no se use entorno virtual se pone solo python
        subprocess.Popen(['python', 'norm_data.py']) #Se pone la ubicación de python.exe del Env, en caso que no se use entorno virtual se pone solo python
    
    if(hora == '3' and minuto == '0'):
        if(fecha_actual == fechaConsulta):
            fechaConsulta = fechaUltimoEnt + deltaDias

            timesfuture = [1,24]

            try: 
                train_models(stations2forecast ,timesfuture, False)
            except Exception as e:
                print("Ocurrió una excepción, no se logro hacer entranamineto semanal", e)



    time.sleep(60)
            