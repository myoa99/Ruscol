# Weather ETL Pipeline & Analytics Dashboard

Проект по сборке сквозного ETL-пайплайна обработки метеорологических данных с валидацией качества (DQ), версионированием контрактов данных и интерактивной визуализацией в Metabase.

---

## 🛠 Архитектура и стек технологий

- **Язык разработки:** Python 3.10+ (`pandas`, `pytest`, `pyyaml`, `psycopg2-binary`)
- **База данных:** PostgreSQL 16 (в Docker-контейнере)
- **BI / Визуализация:** Metabase (в Docker-контейнере)
- **Оркестрация и контейнеризация:** Docker Compose, Python Pipeline Orchestrator

---

## ⚙️ Настройка портов и сети Docker

Во избежание конфликтов портов с локально установленными службами Windows/Linux переназначены внешние порты:

| Сервис | Внутренний порт Docker | Внешний порт (Host) | URL / Подключение |
|---|---|---|---|
| **PostgreSQL** | `5432` | **`5434`** | `localhost:5434` (из Python на хосте) / `postgres:5432` (внутри Docker) |
| **Metabase** | `3000` | **`3001`** | `http://localhost:3001` (в браузере) |

---

## 🚀 Быстрый запуск проекта

### 1. Запуск инфраструктуры Docker

Поднимите PostgreSQL и Metabase одной командой:

```bash
docker compose up -d
```

Проверьте статус запущенных контейнеров:

```bash
docker compose ps
```

Оба сервиса (`weather_postgres` и `weather_metabase`) должны иметь статус `Up` / `running`.

---

### 2. Запуск ETL-пайплайна

Выполните полный цикл обработки данных (Extract → Transform → DQ Check → Load to PostgreSQL):

```bash
python -m src.pipeline --config configs/variant_02.yml --mode full
```

Пайплайн выполнит:
1. Выгрузку сырых данных (`src/extract.py`).
2. Формирование витрины `mart_daily` (`src/build_mart.py`).
3. Валидацию Data Quality и соответствия Data Contract v0.2 (`src/dq.py`).
4. Загрузку итоговой витрины в PostgreSQL (`src/load.py`).

---

### 3. Настройка BI-дашборда в Metabase

1. Перейдите в браузере по адресу: **`http://localhost:3001`**.
2. Подключите базу данных PostgreSQL со следующими параметрами:
   - **Database type:** PostgreSQL
   - **Host:** `postgres` *(имя контейнера в Docker-сети)*
   - **Port:** `5432`
   - **Database name:** `analytics`
   - **Username:** `student`
   - **Password:** `student_pw`
3. Соберите дашборд из 3 ключевых визуализаций:
   - **Line Chart:** Динамика температуры (`temp_mean`) по дням.
   - **Bar Chart:** Максимальная скорость ветра (`wind_speed_max`) по городам.
   - **Area / Table:** Общий объем осадков (`precip_sum`) по датам.

---

## 📂 Структура проекта

```
.
├── configs/
│   └── variant_02.yml          # Конфигурация пайплайна и подключения к БД (порт 5434)
├── docs/
│   ├── Data_Contract.md        # Спецификация Data Contract (v0.2)
│   ├── data_dictionary.md      # Бизнес-словарь витрины данных
│   ├── dq_report.md            # Отчет проверок Data Quality
│   └── bi/                     # Артефакты BI-дашборда (скриншоты и описание)
│       ├── README.md
│       ├── dashboard_overview.png
│       └── db_connection.png
├── src/
│   ├── extract.py              # Модуль выгрузки
│   ├── build_mart.py           # Модуль сборки витрины
│   ├── dq.py                   # Модуль Data Quality
│   ├── load.py                 # Модуль загрузки в PostgreSQL
│   └── pipeline.py             # Главный оркестратор
├── tests/
│   └── test_dq.py              # Юнит-тесты качества данных
├── docker-compose.yml          # Конфигурация контейнеров Postgres и Metabase
├── pytest.ini                  # Конфигурация тестирования
└── README.md                   # Инструкция по запуску проекта
```

---

## 🛡 Data Governance & DQ Rules

Проект реализует требования Data Governance:
- **Data Contract (v0.2):** Все колонки типизированы, зафиксированы единицы измерения (°C, мм, м/с), задан часовой пояс UTC.
- **Data Quality:** Проверки непустоты, контроля NULL, уникальности бизнес-ключа (`city_id`, `date`), валидности дат, диапазона значений и соответствия схемы контракту.
- **Persistence:** Данные хранятся в именованных Docker Volumes (`pgdata`, `metabase_data`), переживая пересоздание контейнеров (`docker compose down`).
