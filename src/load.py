import os
import pandas as pd
from sqlalchemy import create_engine

def run_load(execution_date: str, **kwargs):
    file_path = f"/opt/airflow/data/weather_transformed_{execution_date}.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Load Error: Файл не найден: {file_path}")
        
    df = pd.read_csv(file_path)
    
    # Подключение к PostgreSQL внутри Docker-сети
    db_conn = "postgresql+psycopg2://user:password@postgres:5432/weather_db"
    engine = create_engine(db_conn)
    
    df.to_sql("weather_mart", engine, if_exists="append", index=False)
    print(f"Данные успешно загружены в таблицу weather_mart за дату {execution_date}")
    return True
