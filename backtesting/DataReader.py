import requests
import pandas as pd
import time
from datetime import datetime



start_time = datetime.now()

mytime = datetime(2022, 6, 1)
myInterval = "5m"
fileName = "eth_5min_1m.xlsx"

ticker='ETHUSDT'

start=int(time.mktime(mytime.timetuple())) * 1000


ep='https://api.binance.com'
candle = '/api/v3/klines'

start_date=[]
offen=[]
high=[]
low=[]
close=[]
volume=[]


first_params_candle = {'symbol': ticker, 'interval': '1m', 'startTime': start,'limit':1}
r1 =requests.get(ep+candle, params=first_params_candle)


while len(r1.json()) >0:
    first_params_candle = {'symbol': ticker, 'interval': myInterval, 'startTime': start,'limit':1000}
    r1 =requests.get(ep+candle, params=first_params_candle)
    for i in range(0, len(r1.json())):
        print(datetime.fromtimestamp(r1.json()[i][0]/1000),round(float(r1.json()[i][1]), 4))
        start_date.append(datetime.fromtimestamp(r1.json()[i][0]/1000))
        offen.append(round(float(r1.json()[i][1]), 4))
        high.append(round(float(r1.json()[i][2]), 4))
        low.append(round(float(r1.json()[i][3]), 4))
        close.append(round(float(r1.json()[i][4]), 4))
        volume.append(round(float(r1.json()[i][5]), 4))
    if len(r1.json())>0:
        start = r1.json()[-1][6]+1
        print(datetime.fromtimestamp(r1.json()[-1][6]/1000).strftime('%Y%m%d'), '데이터 다운로드 완료')

    else:
        print('완료, 소요시간 : {0}'.format(datetime.now() - start_time))
    time.sleep(1)

tickerline = [ticker]*len(start_date)
chart_data={'datetime': start_date, 'time': start_time, 'open':offen, 'high': high, 'low':low, 'close':close, 'volume':volume}
df= pd.DataFrame(chart_data, columns=['datetime','open','high','low','close','volume'])
df.set_index("datetime", inplace=True)

df.to_excel(fileName)