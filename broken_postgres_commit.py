import sqlite3
import os

db_path = "example.db"
print("Абсолютный путь к БД:", os.path.abspath(db_path))

# 1. Запись данных
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS t(x INT);")
con.commit()

cur.execute("DELETE FROM t;")
con.commit()

cur.execute("INSERT INTO t(x) VALUES (1);")
con.commit()  # ИСПРАВЛЕНИЕ: Фиксация транзакции перед закрытием соединения

con.close()

# 2. Проверка сохранения в новом соединении
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute("SELECT COUNT(*) FROM t;")
count_val = cur.fetchone()[0]
print(f"Количество записей после повторного открытия: {count_val}")

con.close()
assert count_val == 1, "Ошибка: данные не сохранились!"
