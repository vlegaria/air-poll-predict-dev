import pickle
import mlflow
from mlflow.tracking import MlflowClient
import mlflow.sklearn
import mlflow.pyfunc
from utils.utils import *
import json


with open('recomendations.json', 'r') as archivo_json:
    recomendations = json.load(archivo_json)

mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
client = MlflowClient()

def prediction(station, time1hr, target):
    if time1hr:
        time_future = 1
    else:
        time_future = 24
    model_name = "O3-mer_"+str(time_future)+"hr_forecast_model"
    best_model_alias = "champion"
    best_model = mlflow.pyfunc.load_model(f"models:/{model_name}@{best_model_alias}")
    best_model_info = client.get_model_version_by_alias(model_name, best_model_alias)
    best_model_version = best_model_info.version
    best_model_run_id = best_model_info.run_id
    station = station.upper()
    target = 'O3'
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
    norm_predictions = norm_predictions.reshape(-1, 1)
    predictions = scaler.inverse_transform(norm_predictions)
    ozone_value = round(float(predictions),4)
    if ozone_value <= 51:
        categorical_value = "Buena"
    elif ozone_value > 51 and ozone_value <= 95:
        categorical_value = "Regular"
    elif ozone_value > 95 and ozone_value <= 135:
        categorical_value = "Mala"
    elif ozone_value > 135 and ozone_value <= 175:
        categorical_value = "Muy mala"
    else:
        categorical_value = "Extremadamente mala"

    print("The Ozone value for the next hour is", ozone_value, "ppb")
    response = {"nombre_estacion": station.lower(),
                "color_punto": recomendations[categorical_value]["color"], 
                "contaminante": "ozono",
                "valor_contaminante": ozone_value, 
                "unidad": "ppb", 
                "recomendaciones": recomendations[categorical_value]["texto"]}
    print(response)
    
    return response

prediction("mer", True, "ozono")