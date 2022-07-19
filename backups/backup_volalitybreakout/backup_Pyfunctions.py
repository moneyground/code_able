# -*- coding: utf-8 -*-

import pandas as pd
import math
import telegram
import time

bot = telegram.Bot(token= "5453595066:AAHcYjB3wXgykiYCL-jHSrGSvMn8djOXgqw")
chat_id = 1667012769


# 목표가 계산
def cal_target(exchange, symbol):
    data = exchange.fetch_ohlcv(
        symbol=symbol,
        timeframe="1d",
        since=None,
        limit=10
    )

    # 일봉 데이터를 데이터프레임 객체로 변환
    df = pd.DataFrame(
        data=data,
        columns=["datetime", "open", "high", "low", "close", "volume"]
    )
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")
    df.set_index("datetime", inplace=True)

    # 전일 데이터와 금일 데이터로 목표가 계산
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    long_target = today['open'] + (yesterday["high"] - yesterday["low"]) * 0.4
    short_target = today['open'] - (yesterday["high"] - yesterday["low"]) * 0.4
    return long_target, short_target

# 수량 계산 함수
def cal_amount(usdt_balance, cur_price, portion, leverage):
    usdt_trade = usdt_balance * portion
    amount = math.floor(usdt_trade * 10000 / cur_price) / 10000 * leverage
    return amount

# 포지션 진입
def enter_position(exchange, symbol, cur_price, long_target, short_target, amount, position):
    if cur_price > long_target:
        position["type"] = "long"
        position['amount'] = amount
        exchange.create_market_buy_order(symbol=symbol, amount=amount)
        bot.sendMessage(chat_id, "Market buy order created")
        print("Open LONG position at %f" %cur_price)
    elif cur_price < short_target:
        position["type"] = "short"
        position["amount"] = amount
        exchange.create_market_sell_order(symbol=symbol, amount=amount)
        bot.sendMessage(chat_id, "Market sell order created")
        print("Open SHORT position at %f" %cur_price)

# 포지션 종료
def exit_position(exchange, symbol, position):
    amount = position["amount"]
    if position["type"] == "long":
        exchange.create_market_sell_order(symbol=symbol, amount=amount)
    elif position["type"] == "short":
        exchange.create_market_buy_order(symbol=symbol, amount=amount)

# 스탑로스
def setStopLoss(exchange, Ticker, cut_rate):
    time.sleep(0.1)
    # 주문 정보를 읽어온다.
    orders = exchange.fetch_orders(Ticker)

    StopLossOk = False
    for order in orders:

        if order['status'] == "open" and order['type'] == 'stop_market':
            # print(order)
            StopLossOk = True
            print("=====StopLoss order already set.=====")
            break

    # 스탑로스 주문이 없다면 주문을 건다!
    if not StopLossOk:
        time.sleep(1)
        # 잔고 데이터를 가지고 온다.
        balance = exchange.fetch_balance(params={"type": "future"})
        time.sleep(0.1)

        amount = 0
        entryPrice = 0
        leverage = 0
        # 평균 매입단가와 수량을 가지고 온다.
        for posi in balance['info']['positions']:
            if posi['symbol'] == Ticker.replace("/", ""):
                entryPrice = float(posi['entryPrice'])
                amount = float(posi['positionAmt'])
                leverage = float(posi['leverage'])

        # 롱일땐 숏을 잡아야 되고
        side = "sell"
        # 숏일땐 롱을 잡아야 한다.
        if amount < 0:
            side = "buy"

        danger_rate = ((100.0 / leverage) * cut_rate) * 1.0

        # 롱일 경우의 손절 가격을 정한다.
        stopPrice = entryPrice * (1.0 - danger_rate * 0.01)

        # 숏일 경우의 손절 가격을 정한다.
        if amount < 0:
            stopPrice = entryPrice * (1.0 + danger_rate * 0.01)

        params = {
            'stopPrice': stopPrice,
            'closePosition': True
        }

        # 스탑 로스 주문을 걸어 놓는다.
        exchange.create_order(Ticker, 'STOP_MARKET', side, abs(amount), stopPrice, params)
        print("Stop loss set at %f" %stopPrice)
