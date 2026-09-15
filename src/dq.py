import os
import pandas as pd

def run_dq_checks(execution_date: str, **kwargs):
    file_path = f"/opt/airflow/data/weather_transformed_{execution_date}.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"DQ Error: Файл не найден: {file_path}")
        
    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError("DQ Error: Датасет пустой!")
        
    if "temperature" in df.columns:
        if (df["temperature"] < -90).any() or (df["temperature"] > 60).any():
            raise ValueError("DQ Error: Температура вне физических лимитов!")
            
    print(f"Все DQ-проверки успешно пройдены для даты {execution_date}")
    return True
