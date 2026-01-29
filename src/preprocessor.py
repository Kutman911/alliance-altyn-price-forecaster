import pandas as pd
import numpy as np

def clean_data(input_path="data/raw_financial_data.csv", output_path="data/cleaned_data.csv"):
    df = pd.read_csv(input_path, index_col=0, parse_dates=True)

    print(f"Исходное количество строк: {len(df)}")

    # 1. Заполняем пропуски (Forward Fill - берем цену предыдущего дня для выходных)
    df = df.ffill()

    # 2. Удаляем оставшиеся пропуски (в самом начале данных, если они есть)
    df = df.dropna()

    # 3. Добавляем базовые признаки (Returns) - это важно для анализа волатильности
    for col in df.columns:
        df[f'{col}_Return'] = df[col].pct_change()

    df = df.dropna()

    df.to_csv(output_path)
    print(f"Данные очищены и сохранены в {output_path}")
    print(f"Итоговое количество строк: {len(df)}")
    return df

if __name__ == "__main__":
    clean_data()