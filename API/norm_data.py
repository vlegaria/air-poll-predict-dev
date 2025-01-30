import time
import requests
import locale
import pytz
#from utils.utilsGob import *
from utils.utils import *

stations2forecast = ['MER','UIZ']

locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
tz_mexico = pytz.timezone('America/Mexico_City')

hora_actual = datetime.now(tz_mexico)
hora = str(hora_actual.hour)
minuto = str(hora_actual.minute)

print("Se ejuta otro script Norm")
print(hora,":", minuto)

try:
    norm_data_averages(stations2forecast, hora_actual)
except Exception as e:
    print("Ocurrio un problema al normalizar los promedios horarios, ", e)