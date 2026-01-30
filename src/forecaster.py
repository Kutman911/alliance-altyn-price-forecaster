import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_forecast():
    # Загружаем последние очищенные данные
    df = pd.read_csv("data/cleaned_data.csv", index_col=0, parse_dates=True)
    last_price = df['XAU_USD'].iloc[-1]
    last_date = df.index[-1]

    print(f"Стартовая цена (январь 2026): ${last_price:.2f}")

    # Создаем временную шкалу до 2035 года (помесячно)
    future_dates = pd.date_range(start=last_date, periods=121, freq='ME') # 121 чтобы захватить полный период

    scenarios = {
        "Optimistic (Hyperinflation)": 0.12,
        "Base (Structural Shift)": 0.05,
        "Pessimistic (Correction)": -0.02
    }

    forecast_df = pd.DataFrame(index=future_dates)

    for name, growth in scenarios.items():
        # Формула: Price * (1 + r)^(t/12)
        forecast_df[name] = [last_price * (1 + growth)**(i/12) for i in range(len(future_dates))]

    # Визуализация
    plt.figure(figsize=(12, 6))
    for col in forecast_df.columns:
        plt.plot(forecast_df.index, forecast_df[col], label=col)

    plt.axhline(y=5000, color='r', linestyle='--', label='Psychological Level ($5000)')
    plt.title("Прогноз цен на золото для ООО «Альянс Алтын» (2026-2035)")
    plt.ylabel("Цена XAU/USD")
    plt.legend()
    plt.grid(True)
    plt.show()

    print("Прогноз на 1, 3, 5 лет (Базовый сценарий):")
    print(f"1 год (2027): ${forecast_df['Base (Structural Shift)'].iloc[12]:.2f}")
    print(f"3 года (2029): ${forecast_df['Base (Structural Shift)'].iloc[36]:.2f}")
    print(f"5 лет (2031): ${forecast_df['Base (Structural Shift)'].iloc[60]:.2f}")

    return forecast_df # ВАЖНО: возвращаем DataFrame для следующей функции

def export_to_excel(forecast_df):
    # Путь к файлу
    file_path_xlsx = "data/alliance_altyn_forecast_2026_2035.xlsx"

    # 1. Подготовка данных (статистическая чистка)
    forecast_df['Lower_Bound'] = forecast_df['Base (Structural Shift)'] * 0.85
    forecast_df['Upper_Bound'] = forecast_df['Base (Structural Shift)'] * 1.15
    forecast_df.index = forecast_df.index.date # Убираем время, оставляем только дату

    # 2. Создаем Excel writer с движком xlsxwriter
    writer = pd.ExcelWriter(file_path_xlsx, engine='xlsxwriter')
    forecast_df.to_excel(writer, sheet_name='Price Forecast')

    workbook  = writer.book
    worksheet = writer.sheets['Price Forecast']

    # 3. Наводим красоту: Форматы
    header_format = workbook.add_format({'bold': True, 'bg_color': '#FAA83C', 'color': 'white', 'border': 1})
    money_format = workbook.add_format({'num_format': '$#,##0.00'})
    date_format = workbook.add_format({'num_format': 'mmm yyyy'})

    # Применяем форматы к колонкам
    worksheet.set_column('A:A', 15, date_format) # Дата
    worksheet.set_column('B:F', 18, money_format) # Цены

    # 4. Условное форматирование (Цветовая шкала для цен)
    worksheet.conditional_format('B2:B122', {
        'type': '2_color_scale',
        'min_color': "#FFFAA0",
        'max_color': "#FAA83C"
    })

    # 5. Добавляем график прямо в Excel
    chart = workbook.add_chart({'type': 'line'})

    # Добавляем серии данных на график
    for i in range(1, 4): # Сценарии: Opt, Base, Pess
        chart.add_series({
            'name':       ['Price Forecast', 0, i],
            'categories': ['Price Forecast', 1, 0, 121, 0],
            'values':     ['Price Forecast', 1, i, 121, i],
        })

    chart.set_title({'name': 'Прогноз цен XAU/USD (2026-2035)'})
    chart.set_x_axis({'name': 'Дата'})
    chart.set_y_axis({'name': 'Цена ($)'})

    # Вставляем график рядом с таблицей
    worksheet.insert_chart('H2', chart)

    writer.close()
    print(f"\n--- ФИНАЛ ---")
    print(f"Красивый Excel файл создан: {file_path_xlsx}")

if __name__ == "__main__":
    # Запускаем цепочку
    result_df = generate_forecast()
    export_to_excel(result_df)