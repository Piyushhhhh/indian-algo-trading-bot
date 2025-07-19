import pandas as pd
from utils.plot import plot_trades

def backtest(df: pd.DataFrame, symbol: str, initial_capital: float = 100000, stop_loss_pct: float = 0.03, take_profit_pct: float = 0.06):
    df = df.copy()
    capital = initial_capital
    position = 0
    entry_price = 0
    cash = capital
    trade_log = []
    in_position = False

    for idx, row in df.iterrows():
        signal = row['Signal']
        price = row['Close']

        if signal == 1 and not in_position and cash >= price:
            position = cash // price
            cash -= position * price
            entry_price = price
            in_position = True
            trade_log.append((idx, 'BUY', price, position))
        elif in_position:
            if price <= entry_price * (1 - stop_loss_pct):
                cash += position * price
                trade_log.append((idx, 'SELL (Stop Loss)', price, position))
                position = 0
                in_position = False
            elif price >= entry_price * (1 + take_profit_pct):
                cash += position * price
                trade_log.append((idx, 'SELL (Take Profit)', price, position))
                position = 0
                in_position = False
            elif signal == -1:
                cash += position * price
                trade_log.append((idx, 'SELL (Signal)', price, position))
                position = 0
                in_position = False

    if in_position and position > 0:
        cash += position * df['Close'].iloc[-1]
        trade_log.append((df.index[-1], 'SELL (EOD)', df['Close'].iloc[-1], position))

    final_value = cash
    return_pct = (final_value - initial_capital) / initial_capital * 100
    plot_trades(df, title=f"Trade Chart - {symbol.upper()}")

    return final_value, return_pct, trade_log
