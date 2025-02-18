import json

import pandas as pd

# Путь к CSV-файлу
file_path = 'example.csv'

# Чтение CSV-файла с помощью Pandas
df = pd.read_csv(file_path)
df = 

# Выбор определённой строки по индексу
row_index = 2  # Индекс строки, которую нужно выбрать
selected_row = df.iloc[row_index]

# Преобразование строки в JSON
row_json = selected_row.to_json(orient="index", force_ascii=False)

# Преобразование JSON-строки в словарь (опционально)
row_dict = json.loads(row_json)

# Вывод результата
print(row_json)
print(row_dict)