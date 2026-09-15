# BI Dashboard Artifacts & Documentation (Metabase)

В данной директории содержатся артефакты и документация по дашборду Metabase, разработанному в рамках проекта аналитики метеоданных.

---

## 📌 Состав артефактов

1. **`dashboard_overview.png`** — Скриншот итогового BI-дашборда в Metabase с 3 ключевыми визуализациями:
   - **Line Chart (Температура):** Динамика изменения средней температуры (`temp_mean`) по дням.
   - **Bar Chart (Скорость ветра):** Сравнение максимальной скорости ветра (`wind_speed_max`) по городам.
   - **Area Chart / Table (Осадки):** Суммарный объем осадков (`precip_sum`) в разрезе дат.
2. **`db_connection.png`** — Скриншот успешного подключения Metabase к PostgreSQL через внутреннюю сеть Docker (Host: `postgres`, Port: `5432`).

---

## ⚙️ Параметры подключения Metabase к PostgreSQL

| Параметр | Значение в Docker Network | Значение для внешних клиентов |
|---|---|---|
| **Database Type** | PostgreSQL | PostgreSQL |
| **Host** | `postgres` | `localhost` |
| **Port** | `5432` | `5434` |
| **Database** | `analytics` | `analytics` |
| **User** | `student` | `student` |
| **Password** | `student_pw` | `student_pw` |

---

## 📊 SQL-запросы для построения графиков

### 1. Динамика температуры (`Line Chart`)
```sql
SELECT 
    date,
    city_name,
    temp_mean
FROM mart_daily
ORDER BY date ASC;
```

### 2. Максимальная скорость ветра (`Bar Chart`)
```sql
SELECT 
    city_name,
    MAX(wind_speed_max) AS max_wind_speed
FROM mart_daily
GROUP BY city_name
ORDER BY max_wind_speed DESC;
```

### 3. Распределение осадков (`Area Chart`)
```sql
SELECT 
    date,
    SUM(precip_sum) AS total_precipitation
FROM mart_daily
GROUP BY date
ORDER BY date ASC;
```
