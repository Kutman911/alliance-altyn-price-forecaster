import yfinance as yf
import pandas as pd

def download_financial_data(start_date="2005-01-01"):
    # Тикеры
    tickers = {
        "XAU_USD": "GC=F",   # Золото
        "XAG_USD": "SI=F",   # Серебро
        "DXY": "DX-Y.NYB",   # Индекс доллара
        "BRENT": "BZ=F",     # Нефть
        "UST_10Y": "^TNX"    # Доходность 10-леток
    }

    print(f"Начинаю загрузку данных с {start_date}...")

    # Скачиваем всё сразу одним запросом - это быстрее и стабильнее
    raw_data = yf.download(list(tickers.values()), start=start_date, interval="1d")

    # Выбираем только цены закрытия.
    # В новых версиях yfinance колонка называется 'Close'
    if 'Adj Close' in raw_data.columns:
        data = raw_data['Adj Close']
    else:
        data = raw_data['Close']

    # Переименовываем колонки обратно в наши понятные ключи
    # Создаем маппинг "Тикер Yahoo -> Наше название"
    inv_tickers = {v: k for k, v in tickers.items()}
    data = data.rename(columns=inv_tickers)

    # Сохраняем
    data.to_csv("data/raw_financial_data.csv")
    print("\n--- Успех! ---")
    print(f"Файл сохранен: data/raw_financial_data.csv")
    print(f"Колонки: {list(data.columns)}")
    return data

if __name__ == "__main__":
    download_financial_data()