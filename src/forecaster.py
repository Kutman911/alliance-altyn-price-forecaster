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
    future_dates = pd.date_range(start=last_date, periods=120, freq='ME')

    # Бизнес-логика из ТЗ: Золото > $5000 и системная переоценка
    # Мы заложим среднегодовой рост (CAGR) в 3 сценариях
    scenarios = {
        "Optimistic (Hyperinflation)": 0.12, # +12% в год
        "Base (Structural Shift)": 0.05,     # +5% в год
        "Pessimistic (Correction)": -0.02    # -2% в год
    }

    forecast_df = pd.DataFrame(index=future_dates)

    for name, growth in scenarios.items():
        # Формула сложных процентов: Price * (1 + r)^(t/12)
        forecast_df[name] = [last_price * (1 + growth)**(i/12) for i in range(len(future_dates))]

    # Сохраняем для отчета (Excel/CSV - требование олимпиады)
    forecast_df.to_csv("data/final_forecast_2035.csv")

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

if __name__ == "__main__":
    generate_forecast()