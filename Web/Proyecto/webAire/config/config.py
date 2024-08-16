from decouple import config

TOMTOM_API_KEY = config('TOMTOM_API_KEY')
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY')

DATABASE_HOST = config('DATABASE_HOST')
DATABASE_USER = config('DATABASE_USER')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')
DATABASE_NAME = config('DATABASE_NAME')
DATABASE_PORT = config('DATABASE_PORT')
MLFLOW_PROJECT = config('MLFLOW_PROJECT')