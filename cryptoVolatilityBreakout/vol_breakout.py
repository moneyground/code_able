# -*- coding: utf-8 -*-

import pandas as pd
import math
import telegram
import time

bot = telegram.Bot(token= "5453595066:AAHcYjB3wXgykiYCL-jHSrGSvMn8djOXgqw")
chat_id = 1667012769


# 목표가 계산
def cal_target(exchange, symbol, k):
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
    long_target = today['open'] + (yesterday["high"] - yesterday["low"]) * k
    short_target = today['open'] - (yesterday["high"] - yesterday["low"]) * k
    return long_target, short_target

# 수량 계산
def cal_amount(symbol, usdt_balance, cur_price, portion, leverage):
        usdt_trade = usdt_balance * portion
        if symbol == "BTC/USDT":
            amount = math.floor(usdt_trade * 100000 / cur_price) / 100000 * leverage
            return amount
        elif symbol == "ETH/USDT":
            amount = math.floor(usdt_trade * 10000 / cur_price) / 10000 * leverage
            return amount

# 포지션 진입
def enter_position(exchange, symbol, cur_price, long_target, short_target, amount):
    if cur_price > long_target:
        exchange.create_market_buy_order(symbol=symbol, amount=amount)
        bot.sendMessage(chat_id, "Market buy order created. entry price : %f" %cur_price)
        print("Open LONG position at %f" %cur_price)
        time.sleep(0.2)
        setTakeProfit(exchange, symbol, 2.75)
        setStopLoss(exchange, symbol, 0.7)
    elif cur_price < short_target:
        exchange.create_market_sell_order(symbol=symbol, amount=amount)
        bot.sendMessage(chat_id, "Market sell order created. entry price : %f" %cur_price)
        print("Open SHORT position at %f" %cur_price)
        time.sleep(0.2)
        setTakeProfit(exchange, symbol, 1)
        setStopLoss(exchange, symbol, 0.5)

# 포지션 종료
def exit_position(exchange, symbol):
    exchange.cancel_all_orders(symbol)

    position = exchange.fetch_balance()['info']['positions']
    pos = [p for p in position if p['symbol'] == "ETHUSDT"][0]

    amt = float(pos["positionAmt"])

    if amt > 0:
        exchange.create_market_sell_order(symbol, amt, params={"reduceOnly": True})
    elif amt < 0:
        exchange.create_market_buy_order(symbol, abs(amt), params={"reduceOnly": True})

# Take Profit
def setTakeProfit(exchange, Ticker, cut_rate):
    time.sleep(0.1)

    # 주문 정보를 읽어온다.
    orders = exchange.fetch_orders(Ticker)

    TakeProfitOK = False
    for order_tp in orders:

        if order_tp['status'] == "open" and order_tp['type'] == 'take_profit_market':
            # print(order)
            TakeProfitOK = True
            print("=====TakeProfit order already set.=====")
            break

    # TP 주문이 없다면 주문을 건다!
    if not TakeProfitOK:
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

        take_rate = ((100.0 / leverage) * cut_rate) * 1.0

        # 롱일 경우의 익절 가격을 정한다.
        takePrice = entryPrice * (1.0 + take_rate * 0.01)

        # 숏일 경우의 익절 가격을 정한다.
        if amount < 0:
            takePrice = entryPrice * (1.0 - take_rate * 0.01)

        params = {
            'stopPrice': takePrice,
            'closePosition': True
        }

        # TakeProfit 주문을 걸어 놓는다.
        exchange.create_order(Ticker, 'TAKE_PROFIT_MARKET', side, abs(amount), takePrice, params)
        bot.sendMessage(chat_id, "TakeProfit price : %f" %takePrice)
        print("Take Profit set at %f" %takePrice)

# Stop Loss
def setStopLoss(exchange, Ticker, cut_rate):
    time.sleep(0.1)
    StopLossOk = False

    # 주문 정보를 읽어온다.
    orders = exchange.fetch_orders(Ticker)
    for order_sl in orders:

        if order_sl['status'] == "open" and order_sl['type'] == 'stop_market':
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
        bot.sendMessage(chat_id, "StopLoss price : %f" %stopPrice)
        print("Stop loss set at %f" % stopPrice)
