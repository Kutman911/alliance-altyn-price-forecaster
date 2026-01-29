import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

def train_baseline(input_path="data/cleaned_data.csv"):
    df = pd.read_csv(input_path, index_col=0, parse_dates=True)

    # 1. Выбираем признаки (Features) и цель (Target)
    # Пытаемся предсказать цену Золота на завтра (Shift 1)
    target = 'XAU_USD'
    features = ['XAG_USD', 'DXY', 'BRENT', 'UST_10Y']

    X = df[features]
    y = df[target]

    # Разделяем данные (Time Series Split - нельзя перемешивать!)
    # Берем последние 20% данных для теста
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f"Обучение на периоде: {y_train.index.min()} - {y_train.index.max()}")
    print(f"Тест на периоде: {y_test.index.min()} - {y_test.index.max()}")

    # 2. Инициализация и обучение
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 3. Валидация
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"\n--- Результаты Baseline ---")
    print(f"MAE (Средняя ошибка): ${mae:.2f}")
    print(f"R2 Score (Точность): {r2:.4f}")

    # 4. Сохранение модели
    joblib.dump(model, "src/baseline_model.pkl")
    print("\nМодель сохранена в src/baseline_model.pkl")

    return model

if __name__ == "__main__":
    train_baseline()