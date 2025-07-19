import pandas as pd

def apply_momentum_strategy(df: pd.DataFrame, ma_short=10, ma_long=20) -> pd.DataFrame:
    df = df.copy()
    df['SMA_Short'] = df['Close'].rolling(ma_short).mean()
    df['SMA_Long'] = df['Close'].rolling(ma_long).mean()
    df['Signal'] = 0

    # Buy signal when short MA crosses above long MA
    df.loc[(df['SMA_Short'] > df['SMA_Long']) & (df['SMA_Short'].shift(1) <= df['SMA_Long'].shift(1)), 'Signal'] = 1
    # Sell signal when short MA crosses below long MA
    df.loc[(df['SMA_Short'] < df['SMA_Long']) & (df['SMA_Short'].shift(1) >= df['SMA_Long'].shift(1)), 'Signal'] = -1

    return df
