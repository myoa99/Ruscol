# Data Quality Report
**Итоговый статус:** `WARNING`  
**Всего проверок:** 8

| Проверка | Статус | Сообщение | Детали |
|---|---|---|---|
| `check_not_empty` | **PASS** | Таблица содержит записи | `{'row_count': 7}` |
| `check_not_null` | **PASS** | Пропуски в критических столбцах отсутствуют | `{'city_id': 0, 'date': 0}` |
| `check_unique_key` | **PASS** | Бизнес-ключ уникален | `{'duplicates': 0}` |
| `check_date_format` | **PASS** | Все записи в date являются валидными датами | `{'invalid_dates': 0}` |
| `check_schema_contract` | **WARNING** | Обнаружены нерасписанные в контракте колонки: ['country_code', 'rainy_hours'] | `{'missing': [], 'extra': ['country_code', 'rainy_hours']}` |
| `check_numeric_range_temp_mean` | **PASS** | Все значения temp_mean входят в диапазон [-60.0, 60.0] | `{'invalid_count': 0}` |
| `check_numeric_range_wind_speed_max` | **PASS** | Все значения wind_speed_max входят в диапазон [0.0, 100.0] | `{'invalid_count': 0}` |
| `check_numeric_range_precip_sum` | **PASS** | Все значения precip_sum входят в диапазон [0.0, 500.0] | `{'invalid_count': 0}` |