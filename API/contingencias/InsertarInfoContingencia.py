from config.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np

stations2forecast = ['mer','uiz']

contigen = pd.read_csv('hist_contigencias.csv')

print(contigen.head())

engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
esquema = 'public'
table_name = 'apicalidadaire_prediccion'

for ind in range(contigen.shape[0]):


    #Fecha y hora de activación
    fechaAct = contigen.loc[ind, "Fecha de activación"]
    fechaActSep = fechaAct.split("/")

    diaAct = fechaActSep[0]
    mesAct = fechaActSep[1]
    yearAct = fechaActSep[2]

    horaCompAct = contigen.loc[ind, "Hora de Activacion"]
    horaCompActSep = horaCompAct.split(":")

    horaAct = horaCompActSep[0]

    #Fehca y hora de desactivación
    fechaDes = contigen.loc[ind, "Fecha de desactivación"]
    fechaDesSep = fechaDes.split("/")

    diaDes = fechaDesSep[0]
    mesDes = fechaDesSep[1]
    yearDes = fechaDesSep[2]

    horaCompDes = contigen.loc[ind, "Hora de desactivación"]
    horaCompDesSep = horaCompDes.split(":")

    horaDes = horaCompDesSep[0]

    for indYear in range(int(yearAct),int(yearDes) + 1 ):
        
        for indMonth in range(1,13):

            #Validamos si el mes esta dentro del periodo
            if (indMonth >= int(mesAct) and int(yearAct) == indYear and int(yearAct) != int(yearDes)) or (indYear != int(yearAct) and indYear != int(yearDes)) or (indMonth <= int(mesDes) and int(yearDes) == indYear and int(yearAct) != int(yearDes)) or ( yearDes == yearAct and indMonth >= int(mesAct) and indMonth <= int(mesDes)) :
                
                #Validamos si el dia esta dentro del periodo
                for indDia in range(1,32):
                    if (indDia >= int(diaAct) and int(mesAct) == indMonth and int(mesAct) != int(mesDes)) or (indMonth != int(mesAct) and indMonth != int(mesDes)) or (indDia <= int(diaDes) and int(mesDes) == indMonth and int(mesAct) != int(mesDes)) or ( mesDes == mesAct and indDia >= int(diaAct) and indDia <= int(diaDes)) :
                
                        #Validamos si esta dentro de la hora
                        for indHora in range(0,24):
                            if (indHora >= int(horaAct) and int(diaAct) == indDia and int(diaAct) != int(diaDes)) or (indDia != int(diaAct) and indDia != int(diaDes)) or (indHora <= int(horaDes) and int(diaDes) == indDia and int(diaAct) != int(diaDes)) or ( diaDes == diaAct and indHora >= int(horaAct) and indHora <= int(horaDes)) :
                            
                                for station in stations2forecast:

                                    query = f"update apicalidadaire_{station}_prom_hr set contingency = 1 where year = {indYear} and month = {indMonth} and day = {indDia} and hour = {indHora};"

                                    print(query)
                                    
                                    #ejecutamos query
                                    with engine.connect() as conn:
                                        conn.execute(text(query))
                                        conn.commit()
