from datetime import datetime
import pickle
import joblib
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.models import infer_signature
import mlflow.sklearn
import mlflow.pyfunc
from config.config import MLFLOW_PROJECT, MLFLOW_PWD, MLFLOW_USER, historical_data_1hrfuture, RUTA_MODELOS
from utils.utils import *
from sklearn.model_selection import train_test_split
import os
mlflow.set_tracking_uri(uri="http://0.0.0.0:5000")
#mlflow.set_tracking_uri(uri="http://geopiig.com:5000")

client = MlflowClient()
stations = ['MER', 'UIZ']
times_future = [1,24]
time_steps = 24
target = 'O3'

for time_future in times_future:
    for station in stations:
        print(station)
        # Se carga el archivo de los modelos y del scaler por cada estacion, el target, y el tiempo a predecir
        model_dir = RUTA_MODELOS+'root/web/air-poll-predict-dev/ML/Modelos/best_model_XGBoost_'+str(time_steps)+'timesteps_O3_'+str(time_future)+'timefuture_'+station+'.pkl'
        model_dir = RUTA_MODELOS+'air-poll-predict-dev/ML/Modelos/best_model_XGBoost_'+str(time_steps)+'timesteps_O3_'+str(time_future)+'timefuture_'+station+'.pkl'
        model_dir = 'best_model_XGBoost_'+str(time_steps)+'timesteps_O3_'+str(time_future)+'timefuture_'+station+'.pkl'
        # Obtener la ruta absoluta del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Subir un nivel y acceder a la carpeta 'datos'
        ruta_archivo = os.path.join(script_dir, "..", "Modelos", model_dir)
        # Convertir la ruta en absoluta (para evitar problemas)
        model_dir = os.path.abspath(ruta_archivo)
        print(model_dir)

        loaded_model = joblib.load(model_dir)
        #dir_scaler = RUTA_MODELOS+'air-poll-predict-dev/ML/Scalers/'+station+'_scaler.pkl'
        dir_scaler = station+'_scaler.pkl'
        ruta_archivo = os.path.join(script_dir, "..", "Scaler", model_dir)
        # Convertir la ruta en absoluta (para evitar problemas)
        dir_scaler = os.path.abspath(ruta_archivo)
        with open(dir_scaler, 'rb') as file:
            loaded_scaler = pickle.load(file)

        # Se acceden a los datos de su respectiva base de datos, 
        # se dividen en conjunto de entrenamiento y prueba 
        # Se evalúan las métricas para registrar el desempeño del modelo
        station = station.lower()
        table_name = 'apicalidadaire_'+station+'_norm'
        X, y, df, dates = table_data(table_name, target, station)
        X_seq, y_seq = create_sequences2(X, y, time_steps, time_future)
        X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)
        predicciones_normalizadas = loaded_model.predict(X_test)
        min_val = loaded_scaler.data_min_[4]  # Valor mínimo del O3
        max_val = loaded_scaler.data_max_[4]  # Valor máximo del O3
        # Aplicar la transformación inversa 
        predicciones = predicciones_normalizadas * (max_val - min_val) + min_val
        #y_test_normalizadas = y_test.reshape(-1, 1)
        #y_test = loaded_scaler.inverse_transform(y_test_normalizadas)
        y_test = y_test * (max_val - min_val) + min_val
        metrics_results = metrics(X_test, y_test, predicciones, printData=False)

        MLFLOW_experiment = f"{target} {time_future}hr forecast {station}"
        mlflow.set_experiment(MLFLOW_experiment)
        params = loaded_model.get_params()
        
        # Start an MLflow run
        with mlflow.start_run() as run:
            # Log the hyperparameters
            mlflow.log_params(params)
            run_id = run.info.run_id
            
            # Log scaler as an artifact
            mlflow.log_artifact(dir_scaler, artifact_path="artifacts")

            # Log the metrics
            for metric_name, value in metrics_results.items():
                mlflow.log_metric(metric_name, value)

            # Set a tag that we can use to remind ourselves what this run was for
            info =  f"XGboost model for {target}-{time_future} hr prediction, with the {station}-station data"
            mlflow.set_tag("Training Info",info)

            # Infer the model signature (la forma de la entrada del modelo)
            signature = infer_signature(X_train, loaded_model.predict(X_train))
            model_name = f"{target}-{station}_{time_future}hr_forecast_model"
            # Log the model
            model_info = mlflow.sklearn.log_model(
                sk_model=loaded_model,
                artifact_path=f"{station} station model for {target}-{time_future}hr forecasting",
                signature=signature,
                input_example=X_train,
                registered_model_name=model_name
            )
            # Asignar un alias al modelo
            client.set_registered_model_alias(model_name, "champion", '1')
            # Asignar un tag al modelo registrado
            client.set_model_version_tag(
                name=model_name,
                version= '1',
                key="historicalData",
                value=historical_data_1hrfuture
            )