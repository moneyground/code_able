# -*- coding: utf-8 -*-

import ccxt
import time
import datetime
import vol_breakout
import telegram
from math import floor

bot = telegram.Bot(token= "5453595066:AAHcYjB3wXgykiYCL-jHSrGSvMn8djOXgqw")
chat_id = 1667012769

with open("Binance_API_key.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

# 바이낸스 객체 생성
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

print("Starting Program....")

symbol = "BTC/USDT"
long_target, short_target = vol_breakout.cal_target(binance, symbol, 0.4)


# 잔고 조회
balance = binance.fetch_balance()
usdt = balance["total"]["USDT"]


op_mode = False


# 무한루프
while True:
    now = datetime.datetime.now()

    # 08:50 - 로직 초기화, op_mode 일시 비활성화
    if now.hour == 8 and now.minute == 50 and (0 <= now.second < 10):
        if op_mode is True:
            vol_breakout.exit_position(binance, symbol)
            op_mode = False
        time.sleep(10)

    # 09:00 - 목표가 업데이트, 잔고 업데이트, op_mode 활성화
    if now.hour == 9 and now.minute == 00 and (20 <= now.second < 30):

        # 목표가 업데이트
        long_target, short_target = vol_breakout.cal_target(binance, symbol, 0.4)
        print(now.strftime('%Y-%m-%d %H:%M'),"target price successfully updated")
        bot.sendMessage(chat_id, "Today's Target Price = {0} long {1} short".format(floor(long_target), floor(short_target)))

        # 잔고 조회
        balance = binance.fetch_balance()
        usdt = balance["total"]["USDT"]

        op_mode = True  # op_mode 활성화
        time.sleep(10)


    # 현재가, 구매 가능 수량 (잔고의 100% 자본, 레버리지 10배)
    coin = binance.fetch_ticker(symbol=symbol)
    cur_price = coin["last"]
    amount = vol_breakout.cal_amount(symbol, usdt, cur_price, 1, 25)

    # 포지션 진입
    if op_mode is True:
        vol_breakout.enter_position(binance, symbol, cur_price, long_target, short_target, amount)
        time.sleep(0.1)