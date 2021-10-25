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
    stut1 = ls_oclo[i-3] >= ls_oclo[i-2] and ls_oclo[i-1] <= ls_oclo[i] and Shortpossition == False and Longpossition == False and (ls_oclo[i-2] <= ls_bollow[i-2]  or ls_oclo[i-1] <= ls_bollow[i-1])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i-k] - ls_tend2[i-k]
        Alltendency.append(tendency)
        if tendency > 0:
            tendp = tendp + 1
        k = k + 1
    
    if tendp >= 3 or sum(Alltendency) > 0:
        stut2 = True
    stut3 = stut2 or (Shortpossition == True)  # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Shortpossition == True:
        laststut = (stut1 and stut3) or sellnum * 0.98 > ls_close[i]
    return laststut

def sellmethod2(i):
    stut1 = ls_ochi[i-3] <= ls_ochi[i-2] and ls_ochi[i-1] >= ls_ochi[i] and Shortpossition == False and Longpossition == False and (ls_ochi[i-2] >= ls_bolhigh[i-2] or ls_ochi[i-1] >= ls_bolhigh[i-1])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i-k] - ls_tend2[i-k]
        Alltendency.append(tendency)
        if tendency < 0:
            tendp = tendp + 1
        k = k + 1
    if tendp >= 3 or sum(Alltendency)<0:
        stut2 = True
    stut3 = stut2 or (Longpossition == True) # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Longpossition == True:
        laststut = (stut1 and stut3) or buynum * 1.02 < ls_close[i+5]
    return laststut

def buymethod3(i):
    stut1 = ls_oclo[i-3] >= ls_oclo[i-2] and ls_oclo[i-1] <= ls_oclo[i]  and (ls_oclo[i-2] <= ls_bollow[i-2]  or ls_oclo[i-1] <= ls_bollow[i-1])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i-k] - ls_tend2[i-k]
        Alltendency.append(tendency*k)
        if tendency > 0:
            tendp = tendp + 1
        k = k + 1
    
    if tendp >= 3 or sum(Alltendency) > 0:
        stut2 = True
    stut3 = stut2 or (Shortpossition == True)  # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Shortpossition == True:
        laststut = (stut1 and stut3) or sellnum * 0.98 > ls_close[i]
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
    stut1 = ls_ochi[i-3] <= ls_ochi[i-2] and ls_ochi[i-1] >= ls_ochi[i]  and (ls_ochi[i-2] >= ls_bolhigh[i-2] or ls_ochi[i-1] >= ls_bolhigh[i-1])
    stut2 = False
    k = 1
    tendp = 0
    Alltendency = []
    while k <= 5:
        tendency = ls_tend1[i-k] - ls_tend2[i-k]
        Alltendency.append(tendency*k)
        if tendency < 0:
            tendp = tendp + 1
        k = k + 1

    if tendp >= 3 or sum(Alltendency)<0:
        stut2 = True
    stut3 = stut2 or (Longpossition == True) # 고치기(로직 생각 잘 해서) 포지션이 있는 상태이면 stut2를 신경써서 매도 해야하고, 포지션이 있는 상태이면 신경쓰지 않고 매도해야함
    laststut = (stut1 and stut3)
    if Longpossition == True:
        laststut = (stut1 and stut3) or buynum * 1.02 < ls_close[i]
    # io = 0
    # ii = 0
    # while io <10:
    #     if ls_ochi[i+5-io] > ls_ma[i+5-io]:
    #         ii = ii + 1
    #     io = io + 1
    # if ii >= 7 and Longpossition == True:
    #     laststut = False
    return laststut


mail('Good luck!','Program started !!')

actiontime = -1
summary = ''
Shortpossition = False
Longpossition = False
nfornothing = 30000
MTG = False
ki = 0
summarystat = False
while True:
   try:
        if nowhour() == 19 and nownow() == 1 and summarystat == False:
           possition = 'Todays Report...'
           summary = summary + '\n' +'asset till now'+str(BGDF())
           mail(summary,possition)
           summary = ''
           summarystat = True
        if nownow()%5 == 0:  # 5분마다 한번씩 행동하는 것 (3분으로 나누어 떨어지지 않을 시 행동하지 않음)
            summarystat = False
            if not(actiontime == nownow()):
                actiontime = nownow()
                if MTG == False:
                    etherinfo = GetPD(1)
                    ls_mids = etherinfo.mid.tolist()
                    ls_opens = etherinfo.open.tolist()
                    ls_close = etherinfo.close.tolist()
                    ls_mMm = etherinfo.mMm.tolist()
                    ls_bollow = etherinfo.bollow1.tolist()
                    ls_bolhigh = etherinfo.bolhigh1.tolist()
                    ls_ma = etherinfo.tMA1.tolist()
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
                    if buymethod3(-2) == True:
                        if Shortpossition == False and Longpossition == False:
                            Longpossition = True
                            beforetrade = BGDF()
                            buynum = getcurrent()
                            PN = amountgetter()
                            buybit(PN)
                            summary = summary + str(nowhour())+':'+str(nownow())+'... '+'Longpossition '+'Bought at:'+str(buynum) + '\n'
                        if Shortpossition == True:
                            Shortpossition = False
                            buynum = getcurrent()
                            buybit(PN)
                            aftertrade = BGDF()
                            summary = summary + str(nowhour())+':'+str(nownow())+'... '+'Shortpossition END '+'Bought at:'+str(buynum) + 'Profit is ...' + str(round(100*(aftertrade/beforetrade,2))) +'%'+ '\n'
                    elif sellmethod3(-2) == True:
                        if Shortpossition == False and Longpossition == False:
                            Shortpossition = True
                            beforetrade = BGDF()
                            sellnum = getcurrent()
                            PN = amountgetter()
                            sellbit(PN)
                            summary = summary + str(nowhour())+':'+str(nownow())+'... '+'Shortpossition '+'Sold at:'+str(sellnum) + '\n'
                        if Longpossition == True:
                            Longpossition = False
                            sellnum = getcurrent()
                            sellbit(PN)
                            aftertrade = BGDF()
                            summary = summary + str(nowhour())+':'+str(nownow())+'... '+'Longpossition END '+'Sold at:'+str(sellnum) + 'Profit is ...' + str(round(100*(aftertrade/beforetrade,2))) +'%'+ '\n'

                    if Longpossition == True and ls_low[-2] < buynum*(1-(1/leverage)):                  #
                        summary = 'possition has been winded up'
                        mail(summary,'urgent call')
                        Longpossition = False
                        Shortpossition = False
                    if Shortpossition == True and ls_high[-2] > sellnum*(1+(1/leverage)):               #
                        summary = 'possition has been winded up'
                        mail(summary,'urgent call')
                        Longpossition = False
                        Shortpossition = False

                    if Longpossition == True and ls_high[-2] > ls_bolhigh[-2]:
                        sellnum = getcurrent()
                        sellbit(PN)
                        Longpossition = False
                        summary = summary +  'MAXB ' + str(nowhour())+':'+str(nownow())+'... '+'Longpossition END '+'Sold at:'+str(sellnum) + 'Profit is ...' + str(round(100*(aftertrade/beforetrade,2))) +'%'+ '\n'
                    if Shortpossition == True and ls_low[-2] < ls_bollow[-2]:
                        buynum = getcurrent()
                        buybit(PN)
                        Shortpossition = False
                        summary = summary +  'MAXS ' + str(nowhour())+':'+str(nownow())+'... '+'Shortpossition END '+'Bought at:'+str(buynum) + 'Profit is ...' + str(round(100*(aftertrade/beforetrade,2))) +'%'+ '\n'
                    if Shortpossition == True and ls_vol[-2] > nfornothing and ls_close[-2] > ls_opens[-2]:
                        Shortpossition = False
                        buynum = getcurrent()
                        buybit(PN)
                        time.sleep(1)
                        Longpossition = True
                        beforetrade = BGDF()
                        buynum = getcurrent()
                        PN = amountgetter()
                        buybit(PN)
                        summary = summary + str(nowhour())+':'+str(nownow())+'... '+'switch possition Short -> Long'
                        MTG = True
                        ki = 0
                    if Longpossition == True and ls_vol[-2] > nfornothing and ls_close[-2] < ls_opens[-2]:
                        Longpossition = False
                        sellnum = getcurrent()
                        sellbit(PN)
                        time.sleep(1)
                        Shortpossition = True
                        beforetrade = BGDF()
                        sellnum = getcurrent()
                        sellbit(PN)
                        summary = summary + str(nowhour())+':'+str(nownow())+'... '+'switch possition Long -> Short'
                        MTG = True
                        ki = 0
                ki = ki + 1
        if MTG == True and ki > 7:
            if Longpossition == True and (ls_bolhigh[-2]*1.004 < getcurrent()):
                Longpossition = False
                sellbit(PN)
                summary = summary + 'MTGL-e' + str(nowhour())+':'+str(nownow())+'... '+'Longpossition END '+'Sold at:'+str(sellnum) + 'Profit is ...' + str(round(100*(aftertrade/beforetrade,2))) +'%'+ '\n'
                MTG = False
            if Shortpossition == True and (ls_bollow[-2]*1.004 > getcurrent()):
                Shortpossition = False
                buybit(PN)
                summary = summary + 'MTGS-e' + str(nowhour())+':'+str(nownow())+'... '+'Shortpossition END '+'Bought at:'+str(buynum) + 'Profit is ...' + str(round(100*(aftertrade/beforetrade,2))) +'%'+ '\n'
                MTG = False
        if Longpossition == True and buynum*1.03 < getcurrent():                                #
            sellnum = getcurrent()
            sellbit(PN)
            aftertrade = BGDF()
            Longpossition = False
            summary = summary + str(nowhour())+':'+str(nownow())+'... '+'Longpossition END'+'Sold at:'+str(sellnum) + 'Profit is ...' + str(round(100*(aftertrade/beforetrade,2))) +'%'+ '\n'
        if Shortpossition == True and sellnum * 0.97 > getcurrent():                            #
            buynum = getcurrent()
            buybit(PN)
            aftertrade = BGDF()
            Shortpossition = False
            summary = summary + str(nowhour())+':'+str(nownow())+'... '+'Shortpossition END'+'Bought at:'+str(buynum) + 'Profit is ...' + str(round(100*(aftertrade/beforetrade,2))) +'%'+ '\n'
   except Exception as e:
       print(e)
       time.sleep(1)


#거래 시에는 sellmethod 와 buy method 에 -2 넣고 판단할것 (5분봉이 바뀐 즉시) ---------------------------------완료
# 현재 포지션에 맞는 거래 (숏 잡았을 시 정리 등 ) 고려하여 다시 작성
# 해야할것 -> 7시까지 거래내역을 누적하는 구조를 만들고 이를 7시에 전송하며 이를 하루마다 반복하는 프로그램 작성중 -------------- 완료 