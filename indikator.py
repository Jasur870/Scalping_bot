import pandas as pd

def calculate_indicators(df):
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()
    df['RSI'] = compute_rsi(df['close'], 14)
    df['MACD'], df['MACD_signal'] = compute_macd(df['close'])
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = compute_bollinger_bands(df['close'])
    df['StochRSI'] = compute_stoch_rsi(df['RSI'])
    return df

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_macd(series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def compute_bollinger_bands(series, period=20, std_factor=2):
    middle = series.rolling(window=period).mean()
    std_dev = series.rolling(window=period).std()
    upper = middle + (std_factor * std_dev)
    lower = middle - (std_factor * std_dev)
    return upper, middle, lower

def compute_stoch_rsi(rsi_series, period=14):
    min_val = rsi_series.rolling(window=period).min()
    max_val = rsi_series.rolling(window=period).max()
    stoch_rsi = (rsi_series - min_val) / (max_val - min_val)
    return stoch_rsi * 100

def get_support_resistance(df):
    support = df['low'].rolling(window=10).min().iloc[-1]
    resistance = df['high'].rolling(window=10).max().iloc[-1]
    return {"support": round(support, 2), "resistance": round(resistance, 2)}