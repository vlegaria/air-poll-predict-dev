import time
import requests

#from utils.utilsGob import *
from utils.utils import *

stations2forecast = ['MER','UIZ']


hora_actual = datetime.now()
hora = str(hora_actual.hour)
minuto = str(hora_actual.minute)

print("Se ejuta otro script Norm")
print(hora,":", minuto)

try:
    norm_data_averages(stations2forecast, hora_actual)
except Exception as e:
    print("Ocurrio un problema al normalizar los promedios horarios, ", e)