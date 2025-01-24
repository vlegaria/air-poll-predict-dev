from config.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np
import datetime

stations2forecast = ['mer','uiz']

contigen = pd.read_csv('hist_contigencias.csv')

print(contigen.head())

engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
esquema = 'public'
table_name = 'apicalidadaire_prediccion'

for ind in range(contigen.shape[0]):

    #Fecha de activacion
    fechaAct = contigen.loc[ind, "Fecha de activación"]
    fechaActSep = fechaAct.split("/")

    diaAct = int(fechaActSep[0])
    mesAct = int(fechaActSep[1])
    yearAct = int(fechaActSep[2])

    horaCompAct = contigen.loc[ind, "Hora de Activacion"]
    horaCompActSep = horaCompAct.split(":")

    horaAct = int(horaCompActSep[0])

    fechaAct = datetime.datetime(yearAct,mesAct,diaAct,horaAct)

    #Fecha de desactivación

    fechaDes = contigen.loc[ind, "Fecha de desactivación"]
    fechaDesSep = fechaDes.split("/")

    diaDes = int(fechaDesSep[0])
    mesDes = int(fechaDesSep[1])
    yearDes = int(fechaDesSep[2])

    horaCompDes = contigen.loc[ind, "Hora de desactivación"]
    horaCompDesSep = horaCompDes.split(":")

    horaDes = int(horaCompDesSep[0])

    fechaDes = datetime.datetime(yearDes,mesDes,diaDes,horaDes)

    duracion = fechaDes - fechaAct

    duracionHours = int((duracion.total_seconds())/3600)

    for hora in range(duracionHours + 1):

        deltaHora = datetime.timedelta(hours=hora)

        fechaDurante = fechaAct + deltaHora

        for station in stations2forecast:

            query = f"update apicalidadaire_{station}_prom_hr set contingency = 1 where year = {fechaDurante.year} and month = {fechaDurante.month} and day = {fechaDurante.day} and hour = {fechaDurante.hour};"

            print(query)

            #ejecutamos query
            with engine.connect() as conn:
                conn.execute(text(query))
                conn.commit()

            query = f"update apicalidadaire_{station}_norm set contingency = 1 where year = {fechaDurante.year} and month = {fechaDurante.month} and day = {fechaDurante.day} and hour = {fechaDurante.hour};"

            print(query)

            #ejecutamos query
            with engine.connect() as conn:
                conn.execute(text(query))
                conn.commit()
