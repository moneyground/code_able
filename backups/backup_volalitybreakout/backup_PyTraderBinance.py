# -*- coding: utf-8 -*-

import ccxt
import time
import datetime
import vol_breakout
import telegram

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

symbol = "ETH/USDT"
long_target, short_target = vol_breakout.cal_target(binance, symbol)


# 잔고 조회
balance = binance.fetch_balance()
usdt = balance["total"]["USDT"]

# 포지션 정보
position = {
    "type" : None,
    "amount" : 0
}
op_mode = False

# 파이참 문제점 발생 방지용

cur_price = None

print("Starting Program....")



# 무한루프
while True:
    now = datetime.datetime.now()

    # 오전 8시 50분에 포지션 청산
    if now.hour == 8 and now.minute == 50 and (0 <= now.second < 10):
        if op_mode is True and position["type"] is not None:
            vol_breakout.exit_position(binance, symbol, position)
            position["type"] = None  # 포지션 타입 초기화
            print(now.strftime('%Y-%m-%d %H:%M'), "position closed")
            bot.sendMessage(chat_id, "position successfully closed.\nBalance : = %d" %int(usdt))
            op_mode = False

    # 목표가 갱신
    if now.hour == 9 and now.minute == 00 and (20 <= now.second < 30):
        long_target, short_target = vol_breakout.cal_target(binance, symbol)
        print(now.strftime('%Y-%m-%d %H:%M'),"target price successfully updated")
        bot.sendMessage(chat_id, "Today's Target Price = {0} long {1} short".format(int(long_target), int(short_target)))
        # 잔고 조회
        balance = binance.fetch_balance()
        usdt = balance["total"]["USDT"]
        op_mode = True
        time.sleep(10)

    # 현재가, 구매 가능 수량 (잔고의 10% 자본, 레버리지 50배)
    coin = binance.fetch_ticker(symbol=symbol)
    cur_price = coin["last"]
    amount = vol_breakout.cal_amount(usdt, cur_price, 0.1, 50)

    # 포지션 진입
    if op_mode is True and position["type"] is None:
        vol_breakout.enter_position(binance, symbol, cur_price, long_target, short_target, amount, position)
        time.sleep(1)
