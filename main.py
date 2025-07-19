import argparse
from data.fetcher import fetch_stock_data
from strategies.momentum import apply_momentum_strategy
from backtest.core import backtest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run backtest on a stock")
    parser.add_argument("--symbol", type=str, default="RELIANCE", help="Stock symbol (e.g., RELIANCE)")
    parser.add_argument("--period", type=str, default="6mo", help="Lookback period (e.g., 1mo, 3mo, 6mo)")
    parser.add_argument("--stop", type=float, default=0.03, help="Stop loss percent (e.g., 0.03 = 3%)")
    parser.add_argument("--target", type=float, default=0.06, help="Take profit percent (e.g., 0.06 = 6%)")

    args = parser.parse_args()

    # Fetch historical data
    data = fetch_stock_data(args.symbol, period=args.period)

    # Apply strategy
    strat_df = apply_momentum_strategy(data)

    # Debug: Print last 20 rows of key indicators
    print(strat_df[['Close', 'SMA_Short', 'SMA_Long', 'RSI', 'Volume', 'AvgVolume', 'Signal']].tail(20))

    # Run backtest
    final_value, return_pct, trades = backtest(
        strat_df,
        args.symbol,
        stop_loss_pct=args.stop,
        take_profit_pct=args.target
    )

    # Report
    print(f"\n💹 Final Portfolio Value: ₹{final_value:,.2f}")
    print(f"📈 Strategy Return: {return_pct:.2f}%")
    print("\n📘 Trade Log:")
    for t in trades:
        print(f" - {t[0].strftime('%Y-%m-%d')} | {t[1]} {t[3]} @ ₹{t[2]:.2f}")
