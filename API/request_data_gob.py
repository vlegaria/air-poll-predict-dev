from utils.utilsGob import *
import time

stations2forecast = ['MER','UIZ']

#Ciclo para adquirir datos cada hora de pagina de gobierno

consultarInfo = True

nearest_street_request(stations2forecast, printData=False)

"""
while True:
    hora_actual = datetime.now()
    hora = str(hora_actual.hour)
    minuto = str(hora_actual.minute)
    print(hora,":", minuto)

    if minuto < 15 and minuto > 0:
        consultarInfo = True

    
    if consultarInfo and minuto > 25:
        consultarInfo = False
        try:
            nearest_street_request(stations2forecast, printData=False)
        except Exception as e:
            print("No se descargaron datos a las: ", hora,":", minuto,". Ocurrió una excepción:", e)

            """