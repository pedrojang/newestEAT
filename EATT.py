from numpy.core.einsumfunc import _einsum_path_dispatcher
import pandas as pd
import ccxt
import numpy as np
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText

apiKey = 'Y3dcAaJ0BtLZdQpk9YTryEaft7wQQNMPZc7UJcZAGLKRbDFbtvw2GkRGVeadkvsL'
secKey = 'DA9aVE2d9fs7QWL6YfDs7Q3mJYHblnhJoPdO4tWjbDw4kGJCXviTSlZNroF99Dk9'



lastBol_low = 0.0
lastBol_high = 0.0
binanceFUTURE = ccxt.binance(config={
    'apiKey': apiKey,
    'secret': secKey,
    'enableRateLimit': True, 
})

binanceFR = ccxt.binance(config={
    'apiKey': apiKey, 
    'secret': secKey,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

markets = binanceFR.load_markets()
symbol = "ETH/USDT"
market = binanceFR.market(symbol)
leverage = 30

resp = binanceFR.fapiPrivate_post_leverage({
    'symbol': market['id'],
    'leverage': leverage
})


balance = binanceFUTURE.fetch_balance(params={"type": "future"})


def btcc():
    btc = binanceFR.fetch_ohlcv(
        symbol="ETH/USDT", 
        timeframe='15m', 
        since=None, 
        limit=162 + 138)


    return btc

def btcc_1h():
    btc = binanceFR.fetch_ohlcv(
        symbol="ETH/USDT", 
        timeframe='1h', 
        since=None, 
        limit=61)


    return btc

def GetPD():
    dff = pd.DataFrame(btcc(), columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    dff['datetime'] = pd.to_datetime(dff['datetime'], unit='ms')
    dff['dec'] = dff['high'] - dff['low']
    dff['RD'] = dff['close'] - dff['open']
    dff['GS'] = dff['dec']/dff['volume']
    dff['uptail'] = dff['high'] - ((dff['open'] + dff['close'])/2 + abs(dff['RD'])/2)
    dff['downtail'] = ((dff['open'] + dff['close'])/2 - abs(dff['RD'])/2) - dff['low']
    dff['open1'] = dff['open'].shift(1)
    dff['high1'] = dff['high'].shift(1)
    dff['low1'] = dff['low'].shift(1)
    dff['close1'] = dff['close'].shift(1)
    dff['volume1'] = dff['volume'].shift(1)
    dff['dec1'] = dff['dec'].shift(1)
    dff['RD1'] = dff['RD'].shift(1)
    dff['uptail1'] = dff['uptail'].shift(1)
    dff['downtail1'] = dff['downtail'].shift(1)
    dff['GS1'] = dff['GS'].shift(1)
    dff.set_index('datetime', inplace=True)
    dff['tMA1'] = dff['close1'].rolling(window=20).mean()
    dff['tMA1'] = dff['tMA1'].round(2)
    dff['std1'] = dff['close1'].rolling(window=20).std()
    dff['tMA2'] = dff['tMA1'].shift(1)
    dff['ttMA1'] = dff['close1'].rolling(window=10).mean()
    dff['ttMA1'] = dff['ttMA1'].round(2)
    
    dff['mid'] = dff['open']/2 + dff['close']/2
    dff['mid1'] = dff['mid'].shift(1)
    dff['tend1'] = dff['tMA1'] - dff['tMA2']
    dff['tend2'] = dff['tend1'].shift(1)
    dff1= dff.dropna()
    dff1['bollow1'] = dff1['tMA1'] - 2*dff1['std1']
    dff1['bollow1'] = dff1['bollow1'].round(2)
    dff1['bolhigh1'] = dff1['tMA1'] + 2*dff1['std1']
    dff1['bolhigh1'] = dff1['bolhigh1'].round(2)
    dff1['mMm'] = dff1['mid'] - dff1['mid1']
    dff1.isnull().sum()
    return dff1


# 고가 - 저가 
def getdec():

    lst = GetPD().dec.tolist()
    return lst

# 시가 - 종가 리스트
def getRD():
    lst = GetPD().RD.tolist()
    return lst

# 시가
def getopen():

    lst = GetPD().open.tolist()
    return lst
# 종가 
def getclose():

    lst = GetPD().close.tolist()
    return lst
# 고가
def gethigh():
    lst = GetPD().high.tolist()
    return lst
#저가 
def getlow():
    lst = GetPD().low.tolist()
    return lst

def mail(text,PN):
    now = datetime.now()
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('pedrojang777@gmail.com','mpgzxiggfdjbarqz')

    msg =  MIMEText(text)
    msg['Subject'] = PN + str(now)

    s.sendmail('pedrojang777@gmail.com','peter000520@naver.com',msg.as_string())

    s.quit()

def nownow():
    now = datetime.now().minute

    return now

def nowhour():
    NH = datetime.now().hour

    return NH

# 선물 계좌 구하기 
def BGDF():
    balance = binanceFUTURE.fetch_balance(params={"type": "future"})

    return balance['USDT']['free']
# 현재가 구하기
def getcurrent():
    symbol = "ETH/USDT"
    btc = binanceFR.fetch_ticker(symbol)
    return btc['last']

def amountgetter():
    money = BGDF()
    if BGDF() >= 30000:
        money = 30000
    amountget = round(money/getcurrent(),6)*0.985
    return amountget

#롱 - 풀매수 -
def buybit(a):
    order = binanceFR.create_market_buy_order(
    symbol=symbol,
    amount=a*leverage,
)

#숏 - 풀매도 -
def sellbit(a):
    order = binanceFR.create_market_sell_order(
    symbol=symbol,
    amount=a*leverage,
)
def sellmethod(i):
    
    stut = ls_mids[i] < ls_mids[i+1] and ls_mids[i+1] < ls_mids[i+2] and ls_mids[i+2] > ls_mids[i+3]  #and ls_mids[i+3] > ls_mids[i+4] 
    stut2 = ls_mids[i] < ls_mids[i+1] and ls_mids[i+1] < ls_mids[i+2] and ls_mids[i+2] > ls_mids[i+3] and ls_close[i+3] < ls_opens[i]
    # stut3 = abs(1-(ls_close[i+4]/ls_opens[i+4])) > 0.0047 or Longpossition == True
    laststut = stut or stut2
    stut4 = ls_opens[i+2] > ls_bolhigh[i+2] or ls_opens[i+3] > ls_bolhigh[i+3]
    return laststut and stut4
def buymethod(i):
    stut = ls_mids[i] > ls_mids[i+1] and ls_mids[i+1] > ls_mids[i+2] and ls_mids[i+2] < ls_mids[i+3] #and ls_mids[i+3] < ls_mids[i+4]
    stut2 = ls_mids[i] > ls_mids[i+1] and ls_mids[i+1] > ls_mids[i+2] and ls_mids[i+2] < ls_mids[i+3] and ls_close[i+3] > ls_opens[i]
    # stut3 = abs(1-(ls_close[i+4]/ls_opens[i+4])) > 0.0047 or Shortpossition == True
    laststut = stut or stut2
    stut4 = ls_opens[i+2] < ls_bollow[i+2] or ls_opens[i+3] < ls_bollow[i+3]
    return laststut and stut4

def timechecker_15min():
    now = datetime.now().minute
    hour = datetime.now().hour
    count_15min = now//15 + hour*4
    return count_15min

def timefinder_15min(a):
    day = 0
    if a < 0:
        while a < 0:
            a = a + 96
            day = day - 1
    t = a//4
    tt = a%4
    thattime = str(t)+ ':' + str(tt*15) + '  day from now...' +str(day)
    return thattime

# GetPD().to_excel("Aloha09-08.xlsx")
etherinfo = GetPD(3)
ls_mids = etherinfo.mid.tolist()
ls_opens = etherinfo.open.tolist()
ls_close = etherinfo.close.tolist()
ls_mMm = etherinfo.mMm.tolist()
ls_bollow = etherinfo.bollow1.tolist()
ls_bolhigh = etherinfo.bolhigh1.tolist()
ls_ma = etherinfo.tMA1.tolist()
ls_tend1 = etherinfo.tend1.tolist()
ls_tend2 = etherinfo.tend2.tolist()
i = 0
proF = 1
Longpossition = False
Shortpossition = False
while i + 4 < len(ls_mids):
    if proF > 1.5:
        proF = 1
        Longpossition = False
        Shortpossition = False
    if sellmethod(i) == True:
        if Longpossition == False and Shortpossition == False:
            sellnum = ls_close[i+4]
            Shortpossition = True
        elif Longpossition == True:
            sellnum = ls_close[i+4]
            proF = proF * ((((sellnum/buynum)-1.0006)*30)+1)
            Longpossition = False
            sellnum = ls_close[i+4]*0.999
            Shortpossition = True
    elif buymethod(i) == True:
        if Longpossition == False and Shortpossition == False:
            buynum = ls_close[i+4]
            Longpossition = True
        elif Shortpossition == True:
            buynum = ls_close[i+4]
            proF = proF * ((((sellnum/buynum)-1.0006)*30)+1)
            Shortpossition = False
            buynum = ls_close[i+4]*1.001
            Longpossition = True
    i = i + 1
    print(timefinder_15min(timechecker_15min()-(len(ls_close)-(i+4))) ,proF ,Longpossition , Shortpossition, round(ls_tend1[i+4] - ls_tend2[i+4], 2), ls_opens[i+2] > ls_bolhigh[i+2] or ls_opens[i+3] > ls_bolhigh[i+3], ls_opens[i+2] < ls_bollow[i+2] or ls_opens[i+3] < ls_bollow[i+3]
     )