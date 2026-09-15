import pandas as pd
import pytest
from src.dq import check_not_empty, check_not_null, check_numeric_range, check_unique_key


# 1. Позитивный тест
def test_check_unique_key_pass():
    df = pd.DataFrame({
        "city_id": ["c1", "c2", "c1"],
        "date": ["2026-04-01", "2026-04-01", "2026-04-02"]
    })
    status, msg, details = check_unique_key(df, ["city_id", "date"])
    assert status == "PASS"
    assert details["duplicates"] == 0


# 2. Негативный тест
def test_check_not_null_fail():
    df = pd.DataFrame({
        "city_id": ["c1", None, "c3"],
        "date": ["2026-04-01", "2026-04-02", "2026-04-03"]
    })
    status, msg, details = check_not_null(df, ["city_id", "date"])
    assert status == "FAIL"
    assert details["city_id"] == 1


# 3. Граничный тест
def test_check_numeric_range_boundary():
    df = pd.DataFrame({
        "temp_mean": [-60.0, 0.0, 60.0, 60.1]  # 60.1 — за пределами
    })
    status, msg, details = check_numeric_range(df, "temp_mean", -60.0, 60.0)
    assert status == "WARNING"
    assert details["invalid_count"] == 1


# 4. Граничный тест для пустой таблицы
def test_check_not_empty_fail():
    df_empty = pd.DataFrame()
    status, msg, _ = check_not_empty(df_empty)
    assert status == "FAIL"
