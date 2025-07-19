import pandas as pd
import numpy as np


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain, index=series.index).rolling(window=period).mean()
    avg_loss = pd.Series(loss, index=series.index).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def apply_momentum_strategy(
    df: pd.DataFrame,
    ma_short: int = 10,
    ma_long: int = 20,
    rsi_period: int = 14,
    rsi_buy_threshold: float = 60.0,
    volume_window: int = 20,
    volume_multiplier: float = 1.2,
) -> pd.DataFrame:
    df = df.copy()

    # Calculate indicators
    df['SMA_Short'] = df['Close'].rolling(ma_short).mean()
    df['SMA_Long'] = df['Close'].rolling(ma_long).mean()
    df['RSI'] = calculate_rsi(df['Close'], period=rsi_period)
    df['AvgVolume'] = df['Volume'].rolling(window=volume_window).mean()

    # Initialize Signal column
    df['Signal'] = 0

    # Buy Signal Logic
    crossover = (
        (df['SMA_Short'] > df['SMA_Long']) &
        (df['SMA_Short'].shift(1) <= df['SMA_Long'].shift(1))
    )

    momentum = df['RSI'] > rsi_buy_threshold
    volume_surge = df['Volume'] > (volume_multiplier * df['AvgVolume'])

    buy_condition = crossover & momentum & volume_surge
    df.loc[buy_condition, 'Signal'] = 1

    # Optional: Add Sell Signal logic (e.g., bearish crossover)
    sell_condition = (
        (df['SMA_Short'] < df['SMA_Long']) &
        (df['SMA_Short'].shift(1) >= df['SMA_Long'].shift(1))
    )
    df.loc[sell_condition, 'Signal'] = -1

    return df
