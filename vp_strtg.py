import get_data as gd
from  binance.client import Client
import pandas_ta as ta



def getPoc(ticker):
    df = gd.get_klines(ticker, Client.KLINE_INTERVAL_30MINUTE, "48 hours ago UTC")
    data = df.ta.vp(close = df["Close"], volume = df["Volume"], width=24)
    high_vols = []
    for i in data["total_Volume"].index:
        high_vols.append(data["total_Volume"][i])
    
    high_vol_1 = max(high_vols)

    for i in data.index:
        if data["total_Volume"][i] == high_vol_1:
            mean_fst_hvn = data["mean_Close"][i]
            low_Close_fst = data["low_Close"][i]
            high_Close_fst = data["high_Close"][i]

    
    return mean_fst_hvn

# getPoc("SOLUSDT")
