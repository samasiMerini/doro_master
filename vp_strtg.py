import get_data as gd
from  binance.client import Client
import pandas_ta as ta




def getPoc(ticker):
    df = gd.get_klines(ticker, Client.KLINE_INTERVAL_30MINUTE, "24 hours ago UTC")
    data = df.ta.vp(close = df["Close"], volume = df["Volume"], width=24)
    pos_volume = []
    for i in data["total_Volume"].index:
        pos_volume.append(data["pos_Volume"][i] - data["neg_Volume"][i])
    
    pos_volume_1  = max(pos_volume)
    for i in data.index:
        if data["total_Volume"][i] == pos_volume_1:
            high_pos_hvn =  data["high_Close"][i]
            low_pos_hvn =  data["low_Close"][i]
            mean_pos_hvn =  data["mean_Close"][i]
    pos = 0

    if data["total_Volume"][i] == pos_volume_1:
        for i in df.index:
            close = df["Close"][-1]
            if df["Close"][i] >= low_pos_hvn and df["Close"][i] <= high_pos_hvn and pos == 0:
                pc = ((close / mean_pos_hvn) - 1) * 100
                if pc <= 4:
                    return df["Close"][i]
                    pos = 1

# getPoc("SOLUSDT")
