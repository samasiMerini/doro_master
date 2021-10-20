from  binance.client import Client
import numpy as np
import time
import get_data as gd
import notifications
import vp_strtg
import order  as ordr


# tickers = ["FILUSDT","SOLUSDT","ONEUSDT","TFUELUSDT","ATOMUSDT","FLOWUSDT","BNBUSDT","OMGUSDT","KEEPUSDT","REEFUSDT","FTMUSDT","DOTUSDT","CKBUSDT","MATICUSDT","STXUSDT","FETUSDT","CHRUSDT","ARUSDT","NUUSDT","MANAUSDT","XTZUSDT","CELRUSDT","IRISUSDT","ERNUSDT","ETCUSDT","PERLUSDT","ADAUSDT","EPSUSDT","XRPUSDT","SLPUSDT","XLMUSDT","MBOXUSDT","LINKUSDT","AVAUSDT","KAVAUSDT"]

tickers = ["SOLUSDT","DOTUSDT","ETCUSDT","XRPUSDT","SLPUSDT","BNBUSDT","ICPUSDT","BTCUSDT","FILUSDT"]

print(notifications.sendMessage("Start Application 2 🎉🎉🎉🎉"))
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


def increasePrice(price,pBuy):
    # % increase = Increase ÷ Original Number × 100.
    increase = ((pBuy - price)/price)*100
    print(increase)

def startTrackingCrypto():
    for pds in pdsTOCalculated:
        for ticker  in tickers:
            df = gd.get_klines(ticker, Client.KLINE_INTERVAL_5MINUTE, "84 hours ago UTC")
            touchGreenLine(pds,df,ticker=ticker)

tickerToBuy = {}
tickerToSell = {}

def isTickerBuyOrSellSend(tickerToAdd,type,pds):
    if type == "BUY":
        for ticker in tickerToBuy:
            if ticker == tickerToAdd and pds  == tickerToBuy[ticker]:
                return True

    else:
        for ticker in tickerToSell:
            if ticker == tickerToAdd:
                return True
    return False
def addTickerToBuyList(tickerToAdd,pds):
    tickerToBuy[tickerToAdd] = pds

def addTickerToSellList(tickerToAdd,pds):
    tickerToSell[tickerToAdd] = pds

def removeTicker(ticker,type,pds):
    if type == "BUY":
        for tk in list(tickerToBuy):
            if tk == ticker and pds == tickerToBuy[tk]:
                print("remove ticker")
                del tickerToBuy[tk]
    else:
        for tks in list(tickerToSell):
            if tks == ticker and pds == tickerToSell[tks]:
                print("remove ticker")
                del tickerToSell[tks]

def touchGreenLine(pds,df,ticker):
    result = calculate_Zscore(pds,df)
    score = float(result.tail(1).values)
    message = ""
    close = df["Close"][-1]
    isTimeToBuy = isTickerBuyOrSellSend(ticker,"BUY",pds)
    isTimeToSell = isTickerBuyOrSellSend(ticker,"SELL",pds)
    pocValue = vp_strtg.getPoc(ticker=ticker)
    increase = increasePrice(float(close),float(pocValue))
    
    if score <= -2.5 and score > -4 and not isTimeToBuy:
        message = f"🟢🟢🟢🔔🔔🔔 Chri {ticker}, {round(score,2)} /n  bhad taman  {close} o bi3o  mli iwsal: {pocValue}"
        if score < pocValue and increase > 2.5:
            message  =   message+ "/n" + ordr.startOrder(ticker=ticker)

        addTickerToBuyList(ticker,pds) 
    elif score <= -4 :
        message= f"🟢🟢🟢🔔🔔🔔 Chri 3ad {ticker} ila kayn 💰💰 {round(score,2)}...!"
    elif score > 2.5 and score < 4 and not isTimeToSell:
         message =f"🔴🔴🔴🔔🔔🔔  ila 3adndk  {ticker}  {round(score,2)}, bi3o rah wsal: {close} 💰💰💰 "
         addTickerToSellList(ticker,pds) 
    elif score >= 4:
        message =f"🔴🔴🔴🔔🔔🔔  Ila ba9i 3andk  {ticker} bi3o daba {round(score,2)}, {close}"
    else:
        message = f"tracking {ticker} pds {pds}, realtime price is: {close} and point of control is: {pocValue} ======> {round(score,2)}"

    if  isTimeToBuy or isTimeToSell:
        if (score >-2.5 and score < 2.5):
            removeTicker(ticker,"BUY" if isTimeToBuy else "SELL",pds)

    if "tracking" not in  message: 
        print(notifications.sendMessage(message=message))
    # else:
        # print(message)
        
while True:
    message =("Time: %s" % time.ctime())
    print(message)
    startTrackingCrypto()
    time.sleep(10)


# print("vwapScore : "),
# df  =  pd.DataFrame(result)
# df= df.sort_values(by=['Date'],ascending=False)
#sprint(df)






