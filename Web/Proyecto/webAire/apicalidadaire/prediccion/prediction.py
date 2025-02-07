import pickle
import mlflow
from mlflow.tracking import MlflowClient
import mlflow.sklearn
import mlflow.pyfunc
from apicalidadaire.prediccion.utils.utils import *
import json
import traceback


#with open('apicalidadaire/prediccion/recomendations.json', 'r') as archivo_json:
#    recomendations = json.load(archivo_json)

mlflow.set_tracking_uri(uri="0.0.0.0:5000")
client = MlflowClient()

def prediction(idStation, time1hr, idTarget):

    idPrediccion = None

    print("Entra a función de prediccion")

    try:

        station = selectStation(idStation).loc[0, 'key']

        print("1: " + str(station))

        if time1hr:
            time_future = 1
        else:
            time_future = 24
        model_name = "O3-"+str(station.lower())+"_"+str(time_future)+"hr_forecast_model"
        print(f'model_name: {model_name}')
        best_model_alias = "champion"
        best_model = mlflow.pyfunc.load_model(f"models:/{model_name}@{best_model_alias}")
        best_model_info = client.get_model_version_by_alias(model_name, best_model_alias)
        best_model_version = best_model_info.version
        best_model_run_id = best_model_info.run_id
        station = station.upper()
        target = selectTarget(idTarget).loc[0, 'Contaminante']
        time_steps = 24
        table_name = 'apicalidadaire_'+station+'_norm'
        X, y, df, dates = table_data(table_name, target, station)
        data = ingest(df, target, time_steps)
        norm_predictions = best_model.predict(data)
        artifacts = client.list_artifacts(best_model_run_id, path="artifacts")
        scaler_dir = 'artifacts/'+station.upper()+'_scaler_'+target+'.pkl'
        local_path = mlflow.artifacts.download_artifacts(run_id=best_model_run_id, artifact_path=scaler_dir)
        # Abrir el archivo .pkl descargado
        with open(local_path, "rb") as f:
            scaler = pickle.load(f)
        #norm_predictions = norm_predictions.reshape(-1, 1)
        #predictions = scaler.inverse_transform(norm_predictions)    
        min_val = scaler.data_min_[4]  # Valor mínimo del O3
        max_val = scaler.data_max_[4]  # Valor máximo del O3
        # Aplicar la transformación inversa 
        predictions = norm_predictions * (max_val - min_val) + min_val
        ozone_value = round(float(predictions),4)

        estatus = 0
        if ozone_value <= 51:
            estatus = 1
        elif ozone_value > 51 and ozone_value <= 95:
            estatus = 2
        elif ozone_value > 95 and ozone_value <= 135:
            estatus = 3
        elif ozone_value > 135 and ozone_value <= 175:
            estatus = 4
        else:
            estatus = 5

        EstatusCalidad = selectStatus(estatus)
        unidad = selectUnit(1).loc[0, 'descUnidad']

        print("The Ozone value for the next hour is", ozone_value, "ppb")
        """response = {"nombre_estacion": station.lower(),
                    "color_punto": EstatusCalidad["valorColor"], 
                    "contaminante": "ozono",
                    "valor_contaminante": ozone_value, 
                    "unidad": "ppb", 
                    "recomendaciones": recomendations[categorical_value]["texto"]}"""
        
        idPrediccion = registerPrediction(idStation,idTarget,ozone_value,1,estatus).loc[0, 'idPrediccion']

    except Exception:
            print(traceback.format_exc())
        
    return idPrediccion

#prediction("mer", True, "ozono")