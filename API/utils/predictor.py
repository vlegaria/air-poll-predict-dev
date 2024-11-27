from config.config import TOMTOM_API_KEY, OPENWEATHER_API_KEY, historical_data_1hrfuture, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import make_scorer, mean_squared_error, r2_score, mean_absolute_error
from mlflow.tracking import MlflowClient
from mlflow.models import infer_signature
from config.config import MLFLOW_PROJECT
import mlflow

class ozonePredictor():  

    station = ""
    Xtrain = 0
    Ytrain = 0
    Xtest = 0
    Ytest = 0
    timeFuture = ""
    model = XGBRegressor()
    best_model = ""
    metrics_results = {}


    def __init__(self,station,timeFuture):
        self.station = station
        self.timeFuture = timeFuture

    def prepare_data(self, time_steps):
        #Conexion con postgress     
        engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        esquema = 'public'
        # Recuperar los datos y cargar en un DataFrame
        table_name = 'apicalidadaire_'+self.station+'_norm'

        #Filtrar datos que contengan valor en el trafico 
        query = f"SELECT * FROM {esquema}.{table_name} where not traffic = 'nan';"
        df = pd.read_sql_query(query, engine)
        
        #Quitar filas con NaN
        
        df = df.dropna()

        Y = df['O3']    

        if(self.timeFuture == 1):

            X = df.drop(columns=['idData', 'date', 'month', 'day', 'year', 'minutes', 'contingency', 'O3'])

        if(self.timeFuture == 24):

            X = df.drop(columns=['idData', 'date', 'year', 'minutes', 'contingency', 'O3'])

        #Para que es time_steps?
        Xs, ys = [], []
        for i in range(len(X) - time_steps-int(self.timeFuture)):
            df = X[i:(i + time_steps)]
            array = df.to_numpy()
            # Aplanar el array a un vector
            vector = array.flatten()
            Xs.append(vector)
            ys.append(Y[i + time_steps+int(self.timeFuture)])
        X_seq = np.array(Xs)
        y_seq = np.array(ys)
        # Dividir los datos en conjunto de entrenamiento y prueba
        self.Xtrain, self.Xtest, self.Ytrain, self.Ytest = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

    def train(self):

        # Definir los parámetros para GridSearchCV
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 4, 5],
            'learning_rate': [0.01, 0.05, 0.1]
        }

        retrain_model = GridSearchCV(estimator=self.model, param_grid=param_grid, cv=5, scoring='r2', return_train_score=True)
        
        # Entrenar GridSearchCV
        retrain_model.fit(self.Xtrain, self.Ytrain)

        self.best_model = retrain_model.best_estimator_

    def test(self):
        YPred = self.best_model.predict(self.Xtest)

        n = len(self.Ytest)
        p = self.Xtest.shape[1]

        # Coeficiente de determinación (R-cuadrado)
        r2 = r2_score(self.Ytest, YPred)
        # R-cuadrado ajustado
        r2_adjusted = 1 - (1 - r2) * (n - 1) / (n - p - 1)
        # Error cuadrado medio
        rmse = mean_squared_error(y_true  = self.Ytest, y_pred  = YPred, squared = False)
        # Error Absoluto Medio
        mae = mean_absolute_error(self.Ytest, YPred)

        r2 = round(r2, 6)
        r2_adjusted = round(r2_adjusted, 6)
        rmse = round(rmse, 6)
        mae = round(mae, 6)

        self.metrics_results = {'r2':r2, 'r2adjusted':r2_adjusted,'rmse': rmse, 'mae':mae}

        print(self.metrics_results)


    def implementExperimentMlflow(self,normalizado):

        #Creamos instancio de cliente mlflow
        mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
        client = MlflowClient()

        nombreModeloMlflow = f"O3 {self.timeFuture}hr forecast {self.station}"

        if(normalizado):

            # Si no existe el experimento, lo crea y configura para registrar los parámetros del modelo
            if not mlflow.get_experiment_by_name(nombreModeloMlflow):
                mlflow.create_experiment(name=nombreModeloMlflow)

            # URL y puerto del servidor MLFLOW
            mlflow.set_experiment(nombreModeloMlflow)

            params = self.best_model.get_params()

            # Start an MLflow run
            with mlflow.start_run() as run:

                # Log the hyperparameters
                mlflow.log_params(params)
                run_id = run.info.run_id

                mlflow.log_artifact(f'../ML/Scalers/{self.station}_scaler.pkl', artifact_path="artifacts")

                # Log the loss metric
                for metric_name, value in self.metrics_results.items():
                    mlflow.log_metric(metric_name, value)
                
                # Set a tag that we can use to remind ourselves what this run was for
                info =  f"XGboost model for O3-{self.timeFuture} hr prediction, with the {self.station}-station data"
                mlflow.set_tag("Training Info",info)
                
                # Infer the model signature (la forma de la entrada del modelo)
                signature = infer_signature(self.Xtrain, self.best_model.predict(self.Xtrain))
                model_name = f"O3-{self.station}_{self.timeFuture}hr_forecast_model"
            
                # Log the model
                model_info = mlflow.sklearn.log_model(
                    sk_model=self.best_model,
                    artifact_path=f"{self.station} station model for O3-{self.timeFuture}hr",
                    signature=signature,
                    input_example=self.Xtrain,
                    registered_model_name=model_name
                )

                #
                model_uri = f"runs:/{run_id}/{self.station} station model for O3-{self.timeFuture}hr forecasting".format(run.info.run_id)
                mv = client.create_model_version(model_name, model_uri, run.info.run_id)

                # Asignar un alias al modelo
                client.set_registered_model_alias(model_name, "champion", mv.version)
                # Asignar un tag al modelo registrado
                client.set_model_version_tag(
                    name=model_name,
                    version= '1',
                    key="historicalData",
                    value=historical_data_1hrfuture
                )
        
        else:

            # Si no existe el experimento, lo crea y configura para registrar los parámetros del modelo
            if not mlflow.get_experiment_by_name(nombreModeloMlflow):
                mlflow.create_experiment(name=nombreModeloMlflow)

            # URL y puerto del servidor MLFLOW
            mlflow.set_experiment(nombreModeloMlflow)

            params = self.best_model.get_params()

            # Start an MLflow run
            with mlflow.start_run() as run:

                # Log the hyperparameters
                mlflow.log_params(params)
                run_id = run.info.run_id

                mlflow.log_artifact(f'ML/Scalers/{self.station}_scaler.pkl', artifact_path="artifacts")

                # Log the loss metric
                for metric_name, value in self.metrics_results.items():
                    mlflow.log_metric(metric_name, value)
                
                # Set a tag that we can use to remind ourselves what this run was for
                info =  f"XGboost model for O3-{self.timeFuture} hr prediction, with the {self.station}-station data"
                mlflow.set_tag("Training Info",info)
                
                # Infer the model signature (la forma de la entrada del modelo)
                signature = infer_signature(self.Xtrain, self.best_model.predict(self.Xtrain))
                model_name = f"O3-{self.station}_{self.timeFuture}hr_forecast_model"
            
                # Log the model
                model_info = mlflow.sklearn.log_model(
                    sk_model=self.best_model,
                    artifact_path=f"{self.station} station model for O3-{self.timeFuture}hr",
                    signature=signature,
                    input_example=self.Xtrain,
                    registered_model_name=model_name
                )

                #
                model_uri = f"runs:/{run_id}/{self.station} station model for O3-{self.timeFuture}hr forecasting".format(run.info.run_id)
                mv = client.create_model_version(model_name, model_uri, run.info.run_id)

                # Asignar un alias al modelo
                client.set_registered_model_alias(model_name, "validation_status", mv.version)
                # Asignar un tag al modelo registrado
                client.set_model_version_tag(
                    name=model_name,
                    version= '1',
                    key="historicalData",
                    value=historical_data_1hrfuture
                )

                #Verificar cual es el mejor modelo y si es el mejor lo regristra
                model_name = f"O3-{self.station}_{self.timeFuture}hr_forecast_model "
                best_model_alias = "champion"
                best_model_info = client.get_model_version_by_alias(model_name, best_model_alias)
                best_model_version = best_model_info.version
                best_model_run_id = best_model_info.run_id
                # Acceder a las métricas del mejor modelo
                best_metrics = client.get_run(best_model_run_id).data.metrics
                print("metricas de modelo registrado " + best_metrics)
                # Comparar las métricas del modelo actual con el mejor modelo hasta el momento
                if self.metrics_results["r2adjusted"] > best_metrics["r2adjusted"] and self.metrics_results["rmse"] < best_metrics["rmse"]:
                    #Registra el nuevo modelo como el mejor
                    client.set_registered_model_alias(model_name, best_model_alias, mv.version)
                    client.delete_registered_model_alias(model_name, "validation_status") 
                    client.set_registered_model_alias(model_name, "old_champion", best_model_version)
                else:
                    print("No se mejoró el modelo")