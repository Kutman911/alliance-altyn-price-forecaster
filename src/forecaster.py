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
    # Добавляем интервалы уверенности (статистическая чистка по ТЗ)
    forecast_df['Lower_Bound'] = forecast_df['Base (Structural Shift)'] * 0.85
    forecast_df['Upper_Bound'] = forecast_df['Base (Structural Shift)'] * 1.15

    forecast_df.index.name = 'Date'

    # Сохраняем результат
    file_path = "data/alliance_altyn_forecast_2026_2035.csv"
    forecast_df.to_csv(file_path)
    print(f"\n--- ФИНАЛ ---")
    print(f"Финальная таблица создана: {file_path}")

if __name__ == "__main__":
    # Запускаем цепочку
    result_df = generate_forecast()
    export_to_excel(result_df)