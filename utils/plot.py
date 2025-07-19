import matplotlib.pyplot as plt
import pandas as pd

def plot_trades(df: pd.DataFrame, title: str = "Trade Chart"):
    df = df.copy()
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df['Close'], label='Close Price', color='blue', alpha=0.6)
    if 'SMA_Short' in df.columns:
        plt.plot(df.index, df['SMA_Short'], label='SMA Short', linestyle='--', color='green')
    if 'SMA_Long' in df.columns:
        plt.plot(df.index, df['SMA_Long'], label='SMA Long', linestyle='--', color='orange')
    buy_signals = df[df['Signal'] == 1]
    plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', zorder=5)
    sell_signals = df[df['Signal'] == -1]
    plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', zorder=5)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
