import os
import pandas as pd
from data.fetcher import fetch_stock_data
from strategies.momentum import apply_momentum_strategy
from backtest.core import backtest
from utils.plot import plot_trades

import matplotlib.pyplot as plt

STATIC_RESULTS = 'static-site/results'
os.makedirs(STATIC_RESULTS, exist_ok=True)

def run_and_save(symbol, period='3mo', stop=0.02, target=0.04):
    # Fetch data
    df = fetch_stock_data(symbol, period=period)
    strat_df = apply_momentum_strategy(df)

    # Save strategy dataframe as CSV
    csv_path = os.path.join(STATIC_RESULTS, f'{symbol}-report.csv')
    strat_df.to_csv(csv_path)

    # Save plot as PNG
    plt.figure()
    plot_trades(strat_df, title=f"{symbol} Backtest")
    plot_path = os.path.join(STATIC_RESULTS, f'{symbol}-plot.png')
    plt.savefig(plot_path)
    plt.close()

    # Run backtest (for completeness, not used in static site for now)
    final_value, return_pct, trades = backtest(
        strat_df, symbol, stop_loss_pct=stop, take_profit_pct=target
    )
    print(f"{symbol}: Final Value ₹{final_value:,.2f}, Return {return_pct:.2f}%")

if __name__ == "__main__":
    # Add more symbols as needed
    for symbol in ["INFY", "PAYTM", "SBIN"]:
        run_and_save(symbol, period='3mo', stop=0.02, target=0.04)
