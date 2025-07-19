import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol: str, period: str = '3mo', interval: str = '1d') -> pd.DataFrame:
    ticker = yf.Ticker(symbol + ".NS")
    df = ticker.history(period=period, interval=interval)
    df.dropna(inplace=True)
    df['Symbol'] = symbol
    print(f"✅ Fetched {len(df)} rows for {symbol}")
    return df
