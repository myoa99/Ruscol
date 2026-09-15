import pandas as pd
from io import StringIO

print("--- Шаг 1-2: Исходная проблема ---")
csv_text_broken = "id;value\n1;10\n2;20\n3;30\n"
df_broken = pd.read_csv(StringIO(csv_text_broken))

print("Длина колонок:", len(df_broken.columns))
print("Названия колонок:", df_broken.columns.tolist())
print("Типы данных:\n", df_broken.dtypes)

try:
    print(df_broken["value"].mean())
except KeyError as e:
    print(f"[ОШИБКА]: Столбец {e} не найден в DataFrame!")


print("\n--- Шаг 3-4: Исправленное чтение ---")
df_fixed = pd.read_csv(StringIO(csv_text_broken), sep=";")

print("Первые строки (df.head()):")
print(df_fixed.head())
print("\nТипы столбцов (df.dtypes):")
print(df_fixed.dtypes)
print(f"\nСреднее значение value: {df_fixed['value'].mean()}")


print("\n--- Шаг 5: Ручное тестирование крайних случаев ---")

# Тест 1: Пустая строка
csv_text_2 = "id;value\n1;10\n\n3;30\n"
df_test1 = pd.read_csv(StringIO(csv_text_2), sep=";")
print(f"Тест 1 (Пустая строка): Строк прочитано = {len(df_test1)}")
print(df_test1)

# Тест 2: Пропуск в столбце value
csv_text_3 = "id;value\n1;10\n2;\n3;30\n"
df_test2 = pd.read_csv(StringIO(csv_text_3), sep=";")
print("\nТест 2 (Пропуск значения):")
print(df_test2)
print("Типы столбцов в Тесте 2:\n", df_test2.dtypes)
print(f"Среднее значение value (с пропуском): {df_test2['value'].mean()}")
