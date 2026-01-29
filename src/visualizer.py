import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_trends(input_path="data/cleaned_data.csv"):
    df = pd.read_csv(input_path, index_col=0, parse_dates=True)

    # Настройка стиля (цвета Альянс Алтын: оранжевый и темный)
    plt.style.use('seaborn-v0_8-whitegrid')

    # 1. График цен Золота и Серебра
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Дата')
    ax1.set_ylabel('Золото (XAU/USD)', color='orange')
    ax1.plot(df.index, df['XAU_USD'], color='orange', label='Золото')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Серебро (XAG/USD)', color='gray')
    ax2.plot(df.index, df['XAG_USD'], color='gray', alpha=0.6, label='Серебро')

    plt.title('Динамика цен на драгоценные металлы (2005-2026)')
    plt.show()

    # 2. Матрица корреляций (выбираем только основные цены, без Returns)
    price_cols = ['XAU_USD', 'XAG_USD', 'DXY', 'BRENT', 'UST_10Y']
    corr_matrix = df[price_cols].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn', center=0)
    plt.title('Корреляция факторов влияния')
    plt.show()

    print("Корреляционная матрица:")
    print(corr_matrix['XAU_USD'].sort_values(ascending=False))

if __name__ == "__main__":
    plot_trends()