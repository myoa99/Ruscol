import os
import pandas as pd

file_path = "out.csv"

# Удаляем файл перед первым тестом для чистоты эксперимента
if os.path.exists(file_path):
    os.remove(file_path)

df = pd.DataFrame({"id": [1, 2], "v": [10, 20]})

# ОШИБКА: при каждом запуске данные просто дописываются в конец файла
df.to_csv(file_path, mode="a", header=False, index=False)

# Считываем результат
result_df = pd.read_csv(file_path, names=["id", "v"])
print(f"[ПРОБЛЕМА] Строк в файле после запуска: {len(result_df)}")
