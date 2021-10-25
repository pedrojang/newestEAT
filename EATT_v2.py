from numpy.core.einsumfunc import _einsum_path_dispatcher
from numpy.core.fromnumeric import trace
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


def btcc(day):
    btc = binanceFR.fetch_ohlcv(
        symbol="ETH/USDT", 
        timeframe='5m', 
        since=None, 
        limit=24*12*day+26)


    return btc

def btcc_1h():
    btc = binanceFR.fetch_ohlcv(
        symbol="ETH/USDT", 
        timeframe='1h', 
        since=None, 
        limit=61)


    return btc

def GetPD(day):
    dff = pd.DataFrame(btcc(day), columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
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
    dff['ttMA2'] = dff['ttMA1'].shift(1)
    dff['mid'] = dff['open']/2 + dff['close']/2
    dff['mid1'] = dff['mid'].shift(1)
    dff['tend1'] = dff['ttMA1'] - dff['ttMA2']
    dff['tend2'] = dff['tend1'].shift(1)
    dff1= dff.dropna()
    dff1['bollow1'] = dff1['tMA1'] - 1.8*dff1['std1']
    dff1['bollow1'] = dff1['bollow1'].round(2)
    dff1['bolhigh1'] = dff1['tMA1'] + 1.8*dff1['std1']
    dff1['bolhigh1'] = dff1['bolhigh1'].round(2)
    dff1['mMm'] = dff1['mid'] - dff1['mid1']
    dff1.isnull().sum()
    return dff1

def GetPD1h():
    dff = pd.DataFrame(btcc_1h(), columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
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
    dff['ttMA2'] = dff['ttMA1'].shift(1)
    dff['mid'] = dff['open']/2 + dff['close']/2
    dff['mid1'] = dff['mid'].shift(1)
    dff['tend1'] = dff['ttMA1'] - dff['ttMA2']
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
    if BGDF() > 20000:
        money = 20000
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

def timechecker_5min():
    now = datetime.now().minute
    hour = datetime.now().hour
    count_15min = now//5 + hour*12
    return count_15min

def timefinder_5min(a):
    day = 0
    if a < 0:
        while a < 0:
            a = a + (96*3)
            day = day - 1
    t = a//12
    tt = a%12
    thattime = str(t)+ ':' + str(tt*5) + '  day from now...' +str(day)
    return thattime

def buymethod2(i):
    stut1 = ls_oclo[i+2] >= ls_oclo[i+1+2] and ls_oclo[i+2+2] <= ls_oclo[i+3+2] and Shortpossition == False and Longpossition == False and (ls_oclo[i+3] <= ls_bollow[i+3]  or ls_oclo[i+4] <= ls_bollow[i+4])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i+5-k] - ls_tend2[i+5-k]
        Alltendency.append(tendency)
        if tendency > 0:
            tendp = tendp + 1
        k = k + 1
    
    if tendp >= 3 or sum(Alltendency) > 0:
        stut2 = True
    stut3 = stut2 or (Shortpossition == True)  # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Shortpossition == True:
        laststut = (stut1 and stut3) or sellnum * 0.99 > ls_close[i+5]
    return laststut

def sellmethod2(i):
    stut1 = ls_ochi[i+2] <= ls_ochi[i+1+2] and ls_ochi[i+2+2] >= ls_ochi[i+3+2] and Shortpossition == False and Longpossition == False and (ls_ochi[i+3] >= ls_bolhigh[i+3] or ls_ochi[i+4] >= ls_bolhigh[i+4])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i+5-k] - ls_tend2[i+5-k]
        Alltendency.append(tendency)
        if tendency < 0:
            tendp = tendp + 1
        k = k + 1
    if tendp >= 3 or sum(Alltendency)<0:
        stut2 = True
    stut3 = stut2 or (Longpossition == True) # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Longpossition == True:
        laststut = (stut1 and stut3) or buynum * 1.01 < ls_close[i+5]
    return laststut

def buymethod3(i):
    stut1 = ls_oclo[i+2] >= ls_oclo[i+1+2] and ls_oclo[i+2+2] <= ls_oclo[i+3+2]  and (ls_oclo[i+3] <= ls_bollow[i+3]  or ls_oclo[i+4] <= ls_bollow[i+4])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i+5-k] - ls_tend2[i+5-k]
        Alltendency.append(tendency*k)
        if tendency > 0:
            tendp = tendp + 1
        k = k + 1
    
    if tendp >= 3 or sum(Alltendency) > 0:
        stut2 = True
    stut3 = stut2 or (Shortpossition == True)  # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Shortpossition == True:
        laststut = (stut1 and stut3) or sellnum * 0.98 > ls_close[i+5]
    # io = 0
    # ii = 0
    # while io <10:
    #     if ls_oclo[i+5-io] < ls_ma[i+5-io]:
    #         ii = ii + 1
    #     io = io + 1
    # if ii >= 7 and Shortpossition == True:
    #     laststut = False
    return laststut

def sellmethod3(i):
    stut1 = ls_ochi[i+2] <= ls_ochi[i+1+2] and ls_ochi[i+2+2] >= ls_ochi[i+3+2]  and (ls_ochi[i+3] >= ls_bolhigh[i+3] or ls_ochi[i+4] >= ls_bolhigh[i+4])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i+5-k] - ls_tend2[i+5-k]
        Alltendency.append(tendency*k)
        if tendency < 0:
            tendp = tendp + 1
        k = k + 1

    if tendp >= 3 or sum(Alltendency)<0:
        stut2 = True
    stut3 = stut2 or (Longpossition == True) # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Longpossition == True:
        laststut = (stut1 and stut3) or buynum * 1.02 < ls_close[i+5]
    # io = 0
    # ii = 0
    # while io <10:
    #     if ls_ochi[i+5-io] > ls_ma[i+5-io]:
    #         ii = ii + 1
    #     io = io + 1
    # if ii >= 7 and Longpossition == True:
    #     laststut = False
    return laststut

def buymethod4(i):
    stut1 = ls_oclo[i+2] >= ls_oclo[i+1+2] and ls_oclo[i+2+2] <= ls_oclo[i+3+2]  and (ls_oclo[i+3] <= ls_bollow[i+3]  or ls_oclo[i+4] <= ls_bollow[i+4])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i+5-k] - ls_tend2[i+5-k]
        Alltendency.append(tendency)
        if tendency > 0:
            tendp = tendp + 1
        k = k + 1
    tendp = 5
    if tendp >= 3 or sum(Alltendency) > 0:
        stut2 = True
    stut3 = stut2 or (Shortpossition == True)  # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Shortpossition == True:
        laststut = (stut1 and stut3) or sellnum * 0.98 > ls_close[i+5]
    io = 0
    ii = 0
    while io <10:
        if ls_ochi[i+5-io] > ls_ma[i+5-io]:
            ii = ii + 1
        io = io + 1
    if io >= 10:
        laststut = True
    io = 0
    ii = 0
    while io <10:
        if ls_oclo[i+5-io] < ls_ma[i+5-io]:
            ii = ii + 1
        io = io + 1
    if io >= 10:
        laststut = False
    return laststut

def sellmethod4(i):
    stut1 = ls_ochi[i+2] <= ls_ochi[i+1+2] and ls_ochi[i+2+2] >= ls_ochi[i+3+2]  and (ls_ochi[i+3] >= ls_bolhigh[i+3] or ls_ochi[i+4] >= ls_bolhigh[i+4])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i+5-k] - ls_tend2[i+5-k]
        Alltendency.append(tendency)
        if tendency < 0:
            tendp = tendp + 1
        k = k + 1
    tendp = 5
    if tendp >= 3 or sum(Alltendency)<0:
        stut2 = True
    stut3 = stut2 or (Longpossition == True) # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Longpossition == True:
        laststut = (stut1 and stut3) or buynum * 1.02 < ls_close[i+5]
    io = 0
    ii = 0
    while io <10:
        if ls_ochi[i+5-io] > ls_ma[i+5-io]:
            ii = ii + 1
        io = io + 1
    if io >= 9:
        laststut = False
    io = 0
    ii = 0
    while io <10:
        if ls_oclo[i+5-io] < ls_ma[i+5-io]:
            ii = ii + 1
        io = io + 1
    if io >= 9:
        laststut = True
    return laststut

def MTGl(i):
    MTG = Shortpossition == True and ls_ochi[i+3] > ls_bolhigh[i+3] and ls_ochi[i+4] > ls_bolhigh[i+4] and ls_ochi[i+5] > ls_bolhigh[i+5] and ls_ochi[i+3] < ls_ochi[i+4] < ls_ochi[i+5]
    return MTG
def MTGs(i):
    MTG = Longpossition == True and ls_oclo[i+3] < ls_bollow[i+3] and ls_oclo[i+4] < ls_bollow[i+4] and ls_oclo[i+5] < ls_bollow[i+5] and ls_oclo[i+3] > ls_oclo[i+4] > ls_oclo[i+5]
    return MTG
# GetPD().to_excel("Aloha09-08.xlsx")
etherinfo = GetPD(4)
ls_mids = etherinfo.mid.tolist()
ls_opens = etherinfo.open.tolist()
ls_close = etherinfo.close.tolist()
ls_mMm = etherinfo.mMm.tolist()
ls_bollow = etherinfo.bollow1.tolist()
ls_bolhigh = etherinfo.bolhigh1.tolist()
ls_ma = etherinfo.tMA1.tolist()
ls_ma2 = etherinfo.tMA2.tolist()
ls_tend1 = etherinfo.tend1.tolist()
ls_tend2 = etherinfo.tend2.tolist()
ls_high = etherinfo.high.tolist()
ls_low = etherinfo.low.tolist()
ls_vol =etherinfo.volume.tolist()
ls_ochi = []
ls_oclo = []
i = 0
while i < len(ls_opens):
    if ls_opens[i] <= ls_close[i]:
        ls_ochi.append(ls_close[i])
        ls_oclo.append(ls_opens[i])
    else:
        ls_ochi.append(ls_opens[i])
        ls_oclo.append(ls_close[i])
    i = i + 1
i = 0


# while i < len(ls_oclo):
#     print(ls_ochi[i],' | ',ls_oclo[i])
#     print(timefinder_15min(timechecker_15min()-(len(ls_close)-(i+1))), round(ls_tend1[i],2))
#     i = i + 1
# i = 0
ki = 0
nfornothing = 30000
leverF = 30
Longpossition = False
Shortpossition = False
proF = 1
proFP = 1
MTG = False
while i < (len(ls_oclo) - 5):
    answer = 'NaN '
    if MTG == False:
        if sellmethod3(i):                                              #
            answer = 'sell'
            if Shortpossition == False and Longpossition == False:
                Shortpossition = True
                sellnum = ls_close[i+5]
            if Longpossition == True:
                sellnum = ls_close[i+5]
                proF = proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
                proF = round(proF,4)
                proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
                Longpossition = False
        elif buymethod3(i):                                             #
            answer = 'buy '
            if Shortpossition == False and Longpossition == False:
                Longpossition = True
                buynum = ls_close[i+5]
            if Shortpossition == True:
                buynum = ls_close[i+5]
                proF = proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
                Shortpossition = False
                proF = round(proF,4)
                proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
        if Longpossition == True and buynum*1.03 < ls_high[i+5]:                            #
            sellnum = ls_high[i+5]
            proF = proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
            Longpossition = False
            proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
            answer = 'MAX '
        if Shortpossition == True and sellnum * 0.97 > ls_low[i+5]:                         #
            buynum = ls_low[i+5]
            proF = proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
            Shortpossition = False
            proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
            answer = 'MAX '
        if Longpossition == True and ls_high[i+5] > ls_bolhigh[i+5]:
            sellnum = ls_bolhigh[i+5]
            proF = proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
            Longpossition = False
            proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
            answer = 'MAXB'
        if Shortpossition == True and ls_low[i+5] < ls_bollow[i+5]:
            buynum = ls_bollow[i+5]
            proF = proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
            Shortpossition = False
            proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
            answer = 'MAXS'
        if Shortpossition == True and ls_vol[i+5] > nfornothing and ls_close[i+5] > ls_opens[i+5]:
            Shortpossition = False
            buynum = ls_close[i+5]
            proF= proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
            proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
            Longpossition = True
            buynum = ls_close[i+5]
            MTG = True
            ki = 0
            answer = 'MTGL'
        if Longpossition == True and ls_vol[i+5] > nfornothing and ls_close[i+5] < ls_opens[i+5]:
            Longpossition = False
            sellnum = ls_close[i+5]
            proF= proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
            proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
            Shortpossition = True
            sellnum = ls_close[i+5]
            MTG = True
            ki = 0
            answer = 'MTGS'
    if MTG == True and ki > 7:
        if Longpossition == True and (ls_bolhigh[i+5]*1.004<ls_high[i+5]):
            Longpossition = False
            sellnum = ls_bolhigh[i+5]
            proF = proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
            answer = 'MTGL-e'
            proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
            MTG = False
        if Shortpossition == True and (ls_bollow[i+5]*1.004>ls_low[i+5]):
            Shortpossition = False
            buynum = ls_bollow[i+5]
            proF = proF * ((((sellnum/buynum)-1.0006)*leverF)+1)
            answer = 'MTGS-e'
            proFP = round(proFP + (((((sellnum/buynum)-1.0006)*leverF)+1)-1),4)
            MTG = False
    ki = ki + 1
    if Longpossition == True and ls_low[i+5] < buynum*(1-(1/leverF)):                       #
        proF = 0
    if Shortpossition == True and ls_high[i+5] > sellnum*(1+(1/leverF)):                  #
        proF = 0
    
    answer = answer + ' |' +str(proF)
    print(Shortpossition,'|',Longpossition,'|', answer,'|',timefinder_5min(timechecker_5min()-(len(ls_close)-(i+6))),'|',str(proFP), ls_tend1[i+5] - ls_tend2[i+5], '---',ls_ma[i+5]-ls_ma2[i+5])
    
    i = i + 1


# short/ long dominant 개념의 확립 (20MA의 기울기로써 판단)
# 전체적으로 **적인 상황에서 반대 포지션을 잡는 기준을 정하고, 잡더라도 소극적인 판단을 하도록 설계해야함
# 텐드  1 - 2 가 몇 이상, 이하시 경향이 바뀌는지 체크할것
# 하이 로우를 중심으로 거래할지 결정
# 20MA 근처에 있을 때 텐드 5개로 상승할지 하락할지 예측하는 방법도 고려만 해볼것
# *중요* 지금 이 파일의 백업을 만들고 작업할것 ********************************************************************
# 문제점: 롱 정리시에도 숏을 들고있다고 판단함 --------------------------------------------------------------------------------------------- 해결 됩
# 포지션 잡고 있을 때 최대 수익 달성시 포지션 정리 
# 현재 판단의 지표인 변화율의 5개 합이 음수인지 양수인지를 판단하는 것을 변화율의 개수비교를 통한 판단과 동일선상에 놓고 or 로 연결해서 태스트 해 볼것
# 청산이 되는지 또한 알고리즘을 통해 확인함
# longdominant shortdominant 의 판단은 시봉을 기준으로 할것
# 레버리지를 줄이는 방식으로 청산 피할 수 있으나 초기는 이렇게 해보고 LD 와 SD 판단 기준 설계할것
# buy/ sell method 3을 기준으로 매매 하고, 이를 LD 와 SD 판단 기준 설계하여 (시봉의 기울기를 활용하는 것이 적절해 보임), 
# 볼린저 아래를 5개 이상의 봉이 연속으로 칠때 롱을 잡고 있다면 숏으로의 포지션 전환등

# v3 거래 조건을 method2 로 전환밑 청산 방지 계획(연속된 봉 4개 이상이 볼린저 뚫을 때 매)
# 다시 판단 1분봉을 기준으로 하되 5분봉의 국소고점, 저점등을 사용해 전반적인 하락과 상승을 예측하여 
#20MA 위로 봉이 n개 이상 있으면 상승을 의미 ------ 보류
# 거래량 보고 경향성 판단 (새력의 주도 라는 가정) 랠리에 이상한 판단을 하지 않을 정도로만 
