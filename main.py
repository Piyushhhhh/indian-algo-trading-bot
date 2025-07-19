import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# =====================
# Data Fetching Section
# =====================
def fetch_stock_data(symbol: str, period: str = '3mo', interval: str = '1d'):
    ticker = yf.Ticker(symbol + ".NS")
    df = ticker.history(period=period, interval=interval)
    df.dropna(inplace=True)
    df['Symbol'] = symbol
    print(f"✅ Fetched {len(df)} rows for {symbol}")
    return df

# ========================
# Strategy Logic: Momentum
# ========================
def apply_momentum_strategy(df: pd.DataFrame, ma_short=10, ma_long=20):
    df = df.copy()
    df['SMA_Short'] = df['Close'].rolling(ma_short).mean()
    df['SMA_Long'] = df['Close'].rolling(ma_long).mean()
    df['Signal'] = 0

    # Buy signal when short MA crosses above long MA
    df.loc[(df['SMA_Short'] > df['SMA_Long']) & (df['SMA_Short'].shift(1) <= df['SMA_Long'].shift(1)), 'Signal'] = 1
    # Sell signal when short MA crosses below long MA
    df.loc[(df['SMA_Short'] < df['SMA_Long']) & (df['SMA_Short'].shift(1) >= df['SMA_Long'].shift(1)), 'Signal'] = -1

    return df

# =====================
# Backtest Logic
# =====================
def backtest(df: pd.DataFrame, initial_capital: float = 100000):
    df = df.copy()
    capital = initial_capital
    position = 0  # number of shares
    cash = capital
    trade_log = []

    for idx, row in df.iterrows():
        signal = row['Signal']
        price = row['Close']

        if signal == 1 and cash >= price:
            position = cash // price
            cash -= position * price
            trade_log.append((idx, 'BUY', price, position))
        elif signal == -1 and position > 0:
            cash += position * price
            trade_log.append((idx, 'SELL', price, position))
            position = 0

    final_value = cash + (position * df['Close'].iloc[-1])
    return_pct = (final_value - initial_capital) / initial_capital * 100
    return final_value, return_pct, trade_log

# =====================
# Run Script
# =====================
if __name__ == "__main__":
    data = fetch_stock_data('RELIANCE', period='6mo')
    strat_df = apply_momentum_strategy(data)
    final_value, return_pct, trades = backtest(strat_df)

    print(f"\n💹 Final Portfolio Value: ₹{final_value:,.2f}")
    print(f"📈 Strategy Return: {return_pct:.2f}%")
    print("\n📘 Trade Log:")
    for t in trades:
        print(f" - {t[0].strftime('%Y-%m-%d')} | {t[1]} {t[3]} @ ₹{t[2]:.2f}")
