import ccxt, pandas as pd

def sma_strategy(df, short=50, long=200):
    df = df.copy()
    df["sma_s"] = df["c"].rolling(short).mean()
    df["sma_l"] = df["c"].rolling(long).mean()
    df["signal"] = (df["sma_s"] > df["sma_l"]).astype(int)
    return df

if __name__ == "__main__":
    ex = ccxt.binance()
    ex.set_sandbox_mode(True)
    ohlcv = ex.fetch_ohlcv("BTC/USDT", timeframe="1h", limit=600)
    df = pd.DataFrame(ohlcv, columns=["ts","o","h","l","c","v"])
    df = sma_strategy(df)
    print(df.tail())
