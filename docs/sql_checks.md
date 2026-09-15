# SQL-проверки качества данных витрины (mart_variant_02)

После выполнения скрипта `src/load.py` выполните следующие 5 проверок в СУБД PostgreSQL (через psql, DBeaver или pgAdmin):

### 1. Проверка на непустую таблицу
```sql
SELECT COUNT(*) AS total_rows 
FROM mart_variant_02;
-- Ожидание: total_rows > 0 (соответствует количеству строк в CSV).
Проверка временного диапазона и уникальных дней (Date Range Check)
Цель: Проверить границы временной оси и убедиться в отсутствии аномальных дат.
```
SELECT 
    MIN(date) AS min_date, 
    MAX(date) AS max_date,
    COUNT(DISTINCT date) AS unique_days_count
FROM mart_variant_02;
```
```
Ожидаемый результат: Даты соответствуют периоду прогноза/наблюдений, а unique_days_count равен COUNT(*)
```
3. Проверка на отсутствие NULL в ключевых столбцах (Null Check)
Цель: Убедиться, что бизнес-ключи и критические поля витрины забавлены без пропусков.
```
SELECT COUNT(*) AS null_rows_count
FROM mart_variant_02
WHERE date IS NULL 
   OR city_id IS NULL 
   OR temp_mean IS NULL;
```
```
Ожидаемый результат: null_rows_count = 0
```
4. Проверка уникальности составного бизнес-ключа (Duplicate Check)
Цель: Убедиться в отсутствии дубликатов по сочетанию (date, city_id)
```
SELECT 
    date, 
    city_id, 
    COUNT(*) AS dup_count
FROM mart_variant_02
GROUP BY date, city_id
HAVING COUNT(*) > 1;
```
```
Ожидаемый результат: Запрос возвращает 0 строк.
```
5. Валидация диапазонов и агрегатов KPI (Metric Check)
Цель: Проверить правдоподобность значений агрегированных показателей и отсутствие аномалий.
```
SELECT 
    ROUND(AVG(temp_mean)::numeric, 2) AS avg_temperature,
    MIN(temp_max) AS min_daily_max_temp,
    MAX(temp_max) AS max_daily_max_temp,
    ROUND(SUM(precip_sum)::numeric, 2) AS total_precipitation,
    MAX(wind_speed_max) AS max_wind_speed,
    MIN(rainy_hours) AS min_rainy_hours,
    MAX(rainy_hours) AS max_rainy_hours
FROM mart_variant_02;
```
```
Ожидаемый результат:

avg_temperature в диапазоне [-50; +50] °C;

total_precipitation >= 0;

min_rainy_hours >= 0 и max_rainy_hours <= 24.
```
6. Дополнительная проверка: Контроль отрицательных осадков
Цель: Проверить физическую валидность данных (осадки не могут быть отрицательными).
```
SELECT COUNT(*) AS invalid_precip_count
FROM mart_variant_02
WHERE precip_sum < 0 OR wind_speed_max < 0;
```
```
Ожидаемый результат: invalid_precip_count = 0
```
