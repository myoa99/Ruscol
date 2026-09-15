import argparse
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import yaml

# Импорт ETL-модулей из папки src
from src.extract import main as run_extract
from src.build_mart import main as run_build_mart
from src.dq import run_dq_checks, generate_reports

# Безопасный импорт модуля загрузки (поддержка load.py и load_db.py)
try:
    from src.load import main as run_load
except ImportError:
    from src.load_db import main as run_load

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config(config_path: Path) -> dict:
    """Загрузка YAML-конфигурации."""
    if not config_path.exists():
        raise FileNotFoundError(f"Конфигурационный файл не найден: {config_path.resolve()}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def update_state(status: str, mode: str):
    """Обновление файла состояния пайплайна state.json."""
    state_path = PROJECT_ROOT / "state.json"
    state_data = {
        "last_run_timestamp": datetime.now().isoformat(),
        "last_run_mode": mode,
        "status": status,
        "watermark_date": datetime.now().strftime("%Y-%m-%d")
    }
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state_data, f, ensure_ascii=False, indent=2)


def find_latest_mart_file(mart_dir: Path) -> Path:
    """Поиск самого свежего файла витрины."""
    mart_files = sorted(list(mart_dir.glob("mart_daily_*.csv")))
    if not mart_files:
        raise FileNotFoundError(f"Файлы витрины не найдены в папке: {mart_dir.resolve()}")
    return mart_files[-1]


def run_pipeline(config_path_str: str, mode: str):
    """Главная функция оркестрации."""
    print(f"\n==================================================")
    print(f"[START] Запуск ETL-пайплайна в режиме: {mode.upper()}")
    print(f"==================================================\n")

    config_path = PROJECT_ROOT / config_path_str
    config = load_config(config_path)
    variant_id = config.get("variant", "02")

    # === STEP 1: EXTRACT ===
    print("=== [STEP 1/4] Extract (Выгрузка сырых данных) ===")
    run_extract()

    # === STEP 2: TRANSFORM ===
    print("\n=== [STEP 2/4] Transform (Сборка витрины Mart) ===")
    run_build_mart()

    # === STEP 3: DATA QUALITY ===
    print("\n=== [STEP 3/4] Data Quality (Проверка качества данных) ===")
    mart_dir = PROJECT_ROOT / "data" / "mart" / f"variant_{variant_id}"
    latest_mart_file = find_latest_mart_file(mart_dir)
    print(f"[INFO] Чтение витрины для проверки DQ: {latest_mart_file.name}")
    
    df_mart = pd.read_csv(latest_mart_file)

    # 1. Запуск проверок DQ (получаем словарь report)
    report = run_dq_checks(df_mart, config)
    
    # 2. Сохранение отчетов JSON и Markdown
    json_out = PROJECT_ROOT / "data" / "dq_report.json"
    md_out = PROJECT_ROOT / "docs" / "dq_report.md"
    generate_reports(report, json_out, md_out)

    print(f"[DQ] Итоговый статус: {report['overall_status']}")
    print(f"[DQ] Выполнено проверок: {report['total_checks']}")

    # Прерывание при критических ошибках
    if report["overall_status"] == "FAIL":
        print("[CRITICAL ERROR] DQ-проверки завершились со статусом FAIL! Загрузка в БД отменена.")
        update_state(status="FAILED_DQ", mode=mode)
        return

    # === STEP 4: LOAD ===
    print("\n=== [STEP 4/4] Load (Загрузка в Базу Данных) ===")
    run_load()

    # Фиксация успешного запуска
    update_state(status="SUCCESS", mode=mode)
    print(f"\n==================================================")
    print(f"[COMPLETE] Пайплайн успешно завершен!")
    print(f"==================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Оркестратор ETL-пайплайна weather data")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/variant_02.yml",
        help="Путь к конфигурационному файлу"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["full", "incremental"],
        default="full",
        help="Режим запуска пайплайна (full или incremental)"
    )
    args = parser.parse_args()
    
    run_pipeline(args.config, args.mode)


if __name__ == "__main__":
    main()
