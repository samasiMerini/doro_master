from  binance.client import Client
import numpy as np
import time
import get_data as gd
import notifications
import vp_strtg


tickers = ["FILUSDT","SOLUSDT","ONEUSDT","TFUELUSDT","ATOMUSDT","OMGUSDT","FETUSDT","CELRUSDT","ERNUSDT","ETCUSDT","PERLUSDT","ADAUSDT","EPSUSDT","XRPUSDT","SLPUSDT","MBOXUSDT","LINKUSDT"]
ticker = "FILUSDT"


pdsTOCalculated = [48,199,484]
#pds = 48
def calculate_SMA(ser, pds):

    sma = ser.rolling(window=pds).mean()
    return sma

def calculate_Zscore(pds,df):

    df['mean'] = ((df['Close']*df['Volume']).rolling(pds).sum())/df['Volume'].rolling(pds).sum()
    #mean = sum(volume * close, pds) / sum(volume, pds)
    df['vwapsd'] = np.sqrt(calculate_SMA(pow(df['Close'] - df['mean'], 2), pds))
    #df['z-scoor'] = (df['Close'] - df['mean']) / df['vwapsd']
    return (df['Close'] - df['mean']) / df['vwapsd']




def startTrackingCrypto():
    for pds in pdsTOCalculated:
        for ticker  in tickers:
            df = gd.get_klines(ticker, Client.KLINE_INTERVAL_5MINUTE, "84 hours ago UTC")
            touchGreenLine(pds,df,ticker=ticker)




def touchGreenLine(pds,df,ticker):
    result = calculate_Zscore(pds,df)
    score = float(result.tail(1).values)
    message = ""
    close = df["Close"][-1]
    pocValue = vp_strtg.getPoc(ticker=ticker)
    if score <= -2.5 and close< pocValue :
        message = f"Is time to Buy {ticker}, {round(score,2)} Buy at {close} and Sell when the price achive: {pocValue}"
    elif score < -4 and close < pocValue:
        message= f"Buy {ticker} again {round(score,2)}...!"
    elif score > 2.5:
         message =f"Is time to Sell {ticker}  {round(score,2)}"
    elif score > 4:
        message =f"If you have more {ticker} sell it now {round(score,2)}"
    else:
        message = f"tracking {ticker} pds {pds}, realtime price is: {close} and point of control is: {pocValue} ======> {round(score,2)}"

    if "tracking" not in  message: 
        print(notifications.sendMessage(message=message))
    else:
        print(notifications.sendMessage(message=message))
        
while True:
    print("Time: %s" % time.ctime())
    startTrackingCrypto()
    time.sleep(10)

# print("vwapScore : "),
# df  =  pd.DataFrame(result)
# df= df.sort_values(by=['Date'],ascending=False)
#sprint(df)






