import yfinance as yf
import pandas as pd
from datetime import datetime

def download_financial_data(start_date="2005-01-01"):
    # Список тикеров: Золото, Серебро, Индекс доллара, Нефть Brent, Казначейские облигации 10Y
    tickers = {
        "XAU_USD": "GC=F",   # Золото
        "XAG_USD": "SI=F",   # Серебро
        "DXY": "DX-Y.NYB",   # Индекс доллара
        "BRENT": "BZ=F",     # Нефть
        "UST_10Y": "^TNX"    # Доходность 10-летних облигаций США
    }

    print(f"Начинаю загрузку данных с {start_date}...")

    data = pd.DataFrame()

    for name, ticker in tickers.items():
        df = yf.download(ticker, start=start_date, interval="1d")['Adj Close']
        data[name] = df

    # Сохраняем в папку data
    data.to_csv("data/raw_financial_data.csv")
    print("Данные успешно сохранены в data/raw_financial_data.csv")
    return data

if __name__ == "__main__":
    download_financial_data()