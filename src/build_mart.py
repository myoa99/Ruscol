from datetime import datetime
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def find_latest_normalized_file(norm_dir: Path) -> Path:
    """Ищет самый свежий CSV-файл с нормализованными данными."""
    if not norm_dir.exists():
        raise FileNotFoundError(f"Каталог не найден: {norm_dir.resolve()}")
    csv_files = sorted(list(norm_dir.glob("*.csv")))
    if not csv_files:
        raise FileNotFoundError(f"CSV-файлы не найдены в папке: {norm_dir.resolve()}")
    return csv_files[-1]


def main():
    """Модуль сборки аналитической витрины (Transform)."""
    print("[TRANSFORM] Начало сборки витрины...")

    variant_id = "02"
    norm_dir = PROJECT_ROOT / "data" / "normalized" / f"variant_{variant_id}"
    ref_cities_path = PROJECT_ROOT / "reference" / "cities.csv"
    mart_dir = PROJECT_ROOT / "data" / "mart" / f"variant_{variant_id}"

    # 1. Чтение последних нормализованных данных
    latest_norm_file = find_latest_normalized_file(norm_dir)
    print(f"[INFO] Чтение нормализованных данных из: {latest_norm_file.name}")
    df_norm = pd.read_csv(latest_norm_file)
    print(f"[INFO] Строк в normalized до merge: {len(df_norm)}")

    # 2. Объединение со справочником городов
    if ref_cities_path.exists():
        df_cities = pd.read_csv(ref_cities_path)
        if "city_id" in df_cities.columns and "city_id" in df_norm.columns:
            # Исключаем дублирование колонок при соединении
            cols_to_use = [c for c in df_cities.columns if c == "city_id" or c not in df_norm.columns]
            df_merged = pd.merge(df_norm, df_cities[cols_to_use], on="city_id", how="left")
        else:
            df_merged = df_norm.copy()
    else:
        df_merged = df_norm.copy()

    print(f"[INFO] Строк после merge со справочником: {len(df_merged)}")

    # 3. Распознавание колонки даты/времени (включая 'ts')
    time_candidates = ["ts", "timestamp", "time", "datetime", "dt", "date"]
    time_col = next((col for col in time_candidates if col in df_merged.columns), None)

    if time_col is not None:
        df_merged["date"] = pd.to_datetime(df_merged[time_col]).dt.date
    else:
        raise KeyError(
            f"В файле не найдена колонка даты/времени. Доступные колонки: {list(df_merged.columns)}"
        )

    # 4. Агрегация суточных показателей
    group_keys = [col for col in ["date", "city_id", "city_name", "country_code"] if col in df_merged.columns]

    if "temperature_2m" in df_merged.columns:
        df_mart = df_merged.groupby(group_keys, as_index=False).agg(
            temp_mean=("temperature_2m", "mean"),
            precip_sum=("precipitation", "sum") if "precipitation" in df_merged.columns else ("temperature_2m", "count"),
            wind_speed_max=("wind_speed_10m", "max") if "wind_speed_10m" in df_merged.columns else ("temperature_2m", "count"),
            rainy_hours=("precipitation", lambda x: (x > 0).sum()) if "precipitation" in df_merged.columns else ("temperature_2m", "count")
        )
    else:
        df_mart = df_merged.copy()

    # 5. Расчет 3-дневного скользящего среднего по температуре
    df_mart = df_mart.sort_values(by=["city_id", "date"]).reset_index(drop=True)
    if "temp_mean" in df_mart.columns:
        df_mart["temp_mean"] = df_mart["temp_mean"].round(2)
        df_mart["temp_mean_rolling_3d"] = (
            df_mart.groupby("city_id")["temp_mean"]
            .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
            .round(2)
        )

    if "precip_sum" in df_mart.columns:
        df_mart["precip_sum"] = df_mart["precip_sum"].round(2)

    # 6. Идемпотентность: гарантированная уникальность по Business Key (date, city_id)
    df_mart = df_mart.drop_duplicates(subset=["date", "city_id"], keep="last")

    # 7. Сохранение итогового файла витрины
    mart_dir.mkdir(parents=True, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = mart_dir / f"mart_daily_{timestamp_str}.csv"

    df_mart.to_csv(output_path, index=False)

    print("\n=== Готовая витрина (Mart Daily) ===")
    print(df_mart.head())
    print(f"\n[OK] Витрина успешно сохранена в: {output_path.resolve()}")


if __name__ == "__main__":
    main()
