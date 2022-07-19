# -*- coding: utf-8 -*-

import pandas as pd
import telegram
import ccxt
import datetime
import time

bot = telegram.Bot(token='5386540820:AAE_g3alM3a-Sjeislu_7GaYU8H31lS6CSE')
chat_id = 1667012769

with open("Binance_API_key.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})
symbol = "ETH/USDT"


# 분봉 데이터 조회, 알림 자동전송
def check_trend(exchange, symbol, time):
    data = exchange.fetch_ohlcv(
        symbol=symbol,
        timeframe="5m",
        since=None,
        limit=30
    )

    # 분봉 데이터를 데이터프레임 객체로 변환
    df = pd.DataFrame(
        data=data,
        columns=["datetime", "open", "high", "low", "close", "volume"]
    )
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")
    df.set_index("datetime", inplace=True)

    # 이평선
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['ma15'] = df['close'].rolling(window=15).mean()
    df['ma25'] = df['close'].rolling(window=25).mean()

    # df.to_excel("eth_3y.xlsx")

    past5 = df.iloc[-2]
    present = df.iloc[-1]
    ma5_inclination = (present["ma5"] - past5["ma5"]) / 5




    # 정배열 추세

    # 조건1 : 5분 전 분봉 데이터가 역배열인가?
    if past5["ma5"] > past5["ma10"] > past5["ma15"] > past5["ma25"]:

        # 조건2 : 조건1을 만족하며 현재 분봉 데이터가 역배열인가?
        if present["ma5"] > present["ma10"] > present["ma15"] > present["ma25"]:

            # 조건1, 2를 만족하며 현재 데이터 기준 ma5-ma25 > 0을 만족하는가? -> 정배열 추세
            if present["ma5"] - present["ma25"] > 5:
                bot.sendMessage(chat_id = chat_id, text = "ETH 정배열 추세 포착됨!")
                print(time.strftime('%Y-%m-%d %H:%M'), "정배열 알람 전송됨!")

            # 조건1, 조건2를 만족하지만 ma5 기울기( (5분전 ma5 - 현재 ma5)/15 )가 특정 값보다 작은가? -> 정배열 돌파조짐
            if ma5_inclination < 0.152:
                bot.sendMessage(chat_id=chat_id, text="ETH 정배열 돌파조짐 포착됨!")
                print("정배열 돌파조짐 알람 전송됨!")

        # 조건1을 만족하지만 현재 분봉 기준 ma5<ma25 인가? -> 정배열 돌파
        if present["ma5"] < present["ma10"]:
            bot.sendMessage(chat_id = chat_id, text = "ETH 정배열 돌파 포착됨!")
            print(time.strftime('%Y-%m-%d %H:%M'), "정배열 돌파 알람 전송됨!")

# 역배열 추세

    # 조건1 : 5분전 분봉 데이터가 역배열인가?
    if past5["ma5"] < past5["ma10"] < past5["ma15"] < past5["ma25"]:

        # 조건2 : 조건1을 만족하면서 현재 분봉 데이터가 역배열인가?
        if present["ma5"] < present["ma10"] < present["ma15"] < present["ma25"]:

            # 조건1, 2를 만족하며 ma25-ma5 > 5 을 만족하는가? -> 역배열 추세
            if present["ma25"] - present["ma5"] > 5:
                bot.sendMessage(chat_id = chat_id, text = "ETH 역배열 추세 포착됨!")
                print(time.strftime('%Y-%m-%d %H:%M'), "역배열 알람 전송됨!")

            # 조건1, 조건2를 만족하지만 ma5 기울기( (5분전 ma5 - 현재 ma5)/15 )가 특정 값보다 작은가? -> 역배열 돌파조짐
            if ma5_inclination > -0.152:
                bot.sendMessage(chat_id = chat_id, text = "ETH 역배열 돌파조짐 포착됨!")
                print("역배열 돌파조짐 알람 전송됨!")

        # 조건1을 만족하지만 현재 분봉 기준 ma5>ma25 인가? -> 역배열 돌파
        if present["ma5"] > present["ma10"]:
            bot.sendMessage(chat_id = chat_id, text = "ETH 역배열 돌파 포착됨!")
            print(time.strftime('%Y-%m-%d %H:%M'), "역배열 돌파 알람 전송됨!")


print("system Running...")

while True:
    now = datetime.datetime.now()

    if now.minute % 5 == 1:
        if now.second < 10:
            check_trend(exchange=binance, symbol=symbol, time = now)
            time.sleep(10)