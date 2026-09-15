import os
import pandas as pd

def run_transform(execution_date: str, **kwargs):
    raw_path = f"/opt/airflow/data/weather_raw_{execution_date}.csv"
    transformed_path = f"/opt/airflow/data/weather_transformed_{execution_date}.csv"
    
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Файл с сырыми данными не найден: {raw_path}")
        
    df = pd.read_csv(raw_path)
    if df.empty:
        raise ValueError("Сырой файл пуст!")
        
    df.columns = [str(col).strip().lower() for col in df.columns]
    if "city" in df.columns and "date" in df.columns:
        df = df.drop_duplicates(subset=["city", "date"])
        
    if "temperature" in df.columns:
        df["temperature"] = df["temperature"].fillna(df["temperature"].mean())
        df["temp_fahrenheit"] = df["temperature"] * 9 / 5 + 32
        
    os.makedirs(os.path.dirname(transformed_path), exist_ok=True)
    df.to_csv(transformed_path, index=False)
    print(f"Трансформация завершена. Сохранено в {transformed_path}")
    return transformed_path
