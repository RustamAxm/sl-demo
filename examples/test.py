

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# =============================
# 1. Создаём два датафрейма с разными временными метками
# =============================

# Датафрейм 1: данные с интервалом 1 секунда (0–5 с)
df1 = pd.DataFrame({
    'Time [s]': [
"2025-08-17T07:59:59.828895292+00:00",
"2025-08-17T07:59:59.828896892+00:00",
"2025-08-17T07:59:59.828898492+00:00",
"2025-08-17T07:59:59.828900092+00:00",

    ],
    'Температура A [°C]': [20, 21, 22, 23]
})

# Датафрейм 2: данные с интервалом 1.5 секунды (1.5–6 с)
df2 = pd.DataFrame({
    'Time [s]': [
"2025-08-17T07:59:59.828895000+00:00",
"2025-08-17T07:59:59.829076240+00:00",
"2025-08-17T07:59:59.829529040+00:00",
"2025-08-17T07:59:59.829940000+00:00",
    ],
    'Влажность D [%]': [60, 62, 65, 68]
})

# Проверим исходные данные
print("df1:")
print(df1)
print("\ndf2:")
print(df2)

# Устанавливаем 'Time [s]' как индекс для объединения
df1 = df1.set_index('Time [s]')
df2 = df2.set_index('Time [s]')

# Объединяем по индексу (времени) с сохранением всех точек
common_df = pd.concat([df1, df2], axis=1, sort=True)

# Сбрасываем индекс, чтобы 'Time [s]' стала обычной колонкой
common_df = common_df.reset_index()

# Переименовываем колонку обратно в 'Time [s]'
common_df = common_df.rename(columns={'index': 'Time [s]'})

print("\nОбщий датафрейм:")
print(common_df)

# Создаём график
plt.figure(figsize=(10, 6))
df = common_df
# Построим две линии
plt.plot(df['Time [s]'], df['Температура A [°C]'], label='Температура [°C]', marker='o', linestyle='-', color='red')
plt.plot(df['Time [s]'], df['Влажность D [%]'], label='Влажность [%]', marker='s', linestyle='--', color='blue')

# Подписи и сетка
plt.title('Изменение температуры и влажности во времени', fontsize=14, fontweight='bold')
plt.xlabel('Время [с]', fontsize=12)
plt.ylabel('Значение', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.6)

# Легенда
plt.legend(fontsize=11)

# Автоматическое подстраивание осей
plt.tight_layout()

# Показываем график
plt.show()