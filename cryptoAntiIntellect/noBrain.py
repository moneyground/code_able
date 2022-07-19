from math import floor
import time
import telegram
import random

bot = telegram.Bot("5386540820:AAE_g3alM3a-Sjeislu_7GaYU8H31lS6CSE")
chat_id = 1667012769

# Calculate Amount
def cal_amount(symbol, usdt_balance, cur_price, portion, leverage):
    usdt_trade = usdt_balance * portion
    if symbol == "BTC/USDT":
        amount = floor(usdt_trade * 100000 / cur_price) / 100000 * leverage
        return amount
    elif symbol == "ETH/USDT":
        amount = floor(usdt_trade * 10000 / cur_price) / 10000 * leverage
        return amount

# TakeProfit
def setTakeProfit(exchange, symbol, take_rate):
    time.sleep(0.1)

    if take_rate is None:
        pass
    else:

        # Scanning order information
        orders = exchange.fetch_orders(symbol)

        TakeProfitOK = False
        for order_tp in orders:

            if order_tp['status'] == "open" and order_tp['type'] == 'take_profit_market':
                TakeProfitOK = True
                print("=====TakeProfit order already set.=====")
                break

        # TP 주문이 없다면 주문을 건다!
        if not TakeProfitOK:
            time.sleep(1)
            # 잔고 데이터를 가지고 온다.
            myBalance = exchange.fetch_balance(params={"type": "future"})
            time.sleep(0.1)

            amount = 0
            entryPrice = 0
            leverage = 0

            # 평균 매입단가와 수량을 가지고 온다.
            for posi in myBalance['info']['positions']:
                if posi['symbol'] == symbol.replace("/", ""):
                    entryPrice = float(posi['entryPrice'])
                    amount = float(posi['positionAmt'])
                    leverage = float(posi['leverage'])

            # 롱일땐 숏을 잡아야 되고
            side = "sell"
            # 숏일땐 롱을 잡아야 한다.
            if amount < 0:
                side = "buy"

            take_rate = ((100.0 / leverage) * take_rate) * 1.0

            # 롱일 경우의 익절 가격을 정한다.
            takePrice = entryPrice * (1.0 + take_rate * 0.01)

            # 숏일 경우의 익절 가격을 정한다.
            if amount < 0:
                takePrice = entryPrice * (1.0 - take_rate * 0.01)

            params = {
                'stopPrice': takePrice,
                'closePosition': True
            }

            # create TakeProfit order
            exchange.create_order(symbol, 'TAKE_PROFIT_MARKET', side, abs(amount), takePrice, params)
            bot.sendMessage(chat_id, "TakeProfit price : %f" %takePrice)
            print("Take Profit set at %f" %takePrice)

# StopLoss
def setStopLoss(exchange, symbol, cut_rate):
    time.sleep(0.1)
    StopLossOk = False

    # cut_rate is None -> Do not set StopLoss
    if cut_rate is None:
        pass
    else:

        # Scanning my order information
        orders = exchange.fetch_orders(symbol)
        for order_sl in orders:

            if order_sl['status'] == "open" and order_sl['type'] == 'stop_market':
                # print(order)
                StopLossOk = True
                print("=====StopLoss order already set.=====")
                break

        # set StopLoss if there is no SL order
        if not StopLossOk:
            time.sleep(1)

            # Scanning My Balance Data
            myBalance = exchange.fetch_balance(params={"type": "future"})

            amount = 0
            entryPrice = 0
            leverage = 0

            # Scanning my avgEntryPrice and Amount
            for posi in myBalance['info']['positions']:
                if posi['symbol'] == symbol.replace("/", ""):
                    entryPrice = float(posi['entryPrice'])
                    amount = float(posi['positionAmt'])
                    leverage = float(posi['leverage'])

            # if my side == long -> SL side = short
            side = "sell"
            # if my side == short -> SL side = long
            if amount < 0:
                side = "buy"

            danger_rate = ((100.0 / leverage) * cut_rate) * 1.0

            # set stopPrice if my side == long
            stopPrice = entryPrice * (1.0 - danger_rate * 0.01)

            # set stopPrice if my side == short
            if amount < 0:
                stopPrice = entryPrice * (1.0 + danger_rate * 0.01)

            params = {
                'stopPrice': stopPrice,
                'closePosition': True
            }

            # create StopLoss order
            exchange.create_order(symbol, 'STOP_MARKET', side, abs(amount), stopPrice, params)
            bot.sendMessage(chat_id, "StopLoss price : %f" %stopPrice)
            print("Stop loss set at %f" % stopPrice)

# EnterPosition
def enter_position(exchange, symbol, cur_price, amount, takeRate, cutRate, timme):
    today_pos = random.randint(0, 1)

    if today_pos:

        # order
        exchange.create_market_buy_order(symbol = symbol, amount = amount)

        print(timme.strftime('%Y-%m-%d %H:%M'), "Long position successfully opened.")
        bot.sendMessage(chat_id, "Your Random Position is Long. entryPrice : %f" %cur_price)

        time.sleep(3)

        # SL/TP
        setTakeProfit(exchange, symbol, takeRate)
        setStopLoss(exchange, symbol, cutRate)

    elif not today_pos:

        # order
        exchange.create_market_sell_order(symbol = symbol, amount = amount)

        print(timme.strftime('%Y-%m-%d %H:%M'), "Short position successfully opened.")
        bot.sendMessage(chat_id, "Your Random Position is Short. entryPrice : %f" %cur_price)

        time.sleep(3)

        # SL/TP
        setTakeProfit(exchange, symbol, takeRate)
        setStopLoss(exchange, symbol, cutRate)

# ExitPosition
def exit_position(exchange, symbol, timme):
    exchange.cancel_all_orders(symbol)

    position = exchange.fetch_balance()['info']['positions']
    pos = [p for p in position if p['symbol'] == "ETHUSDT"][0]

    amt = float(pos["positionAmt"])

    if amt > 0:
        exchange.create_market_sell_order(symbol, amt, params={"reduceOnly": True})
    elif amt < 0:
        exchange.create_market_buy_order(symbol, abs(amt), params={"reduceOnly": True})

    print(timme.strftime('%Y-%m-%d %H:%M'), "Position successfully closed ")
