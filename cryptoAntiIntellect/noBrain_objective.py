from math import floor
import telegram
import random
import datetime
from time import sleep


class moneyGround:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol

        position = self.exchange.fetch_balance()['info']['positions']
        pos = [p for p in position if p['symbol'] == self.symbol.replace("/", "")][0]

        self.pos = pos

    def __stoploss_setting(self, cutRate):

        amount = 0
        entryPrice = 0
        leverage = 0

        if self.pos["symbol"] == self.symbol.replace("/", ""):
            entryPrice = float(self.pos["entryPrice"])
            amount = float(self.pos["positionAmt"])
            leverage = float(self.pos['leverage'])

        danger_rate = ((100.0 / leverage) * cutRate) * 1.0



        stopPrice = entryPrice * (1.0 - danger_rate * 0.01)
        if amount < 0:
            stopPrice = entryPrice * (1.0 + danger_rate * 0.01)


        side = "sell"
        if amount < 0:
            side = "buy"


        params_sl = {
            'stopPrice': stopPrice,
            'closePosition': True
        }

        self.exchange.create_order(self.symbol, "STOP_MARKET", side, abs(amount), stopPrice, params_sl)

    def __cal_amount(self):

        leverage = self.pos["leverage"]

        # MyBalance
        balance = self.exchange.fetch_balance()
        usdt = balance["total"]["USDT"]

        # Cryptocurrency Last Price
        coin = self.exchange.fetch_ticker(self.symbol)
        cur_price = coin["last"]

        # Calculate amount
        amount = floor(usdt * 10000 / cur_price) / 10000 * leverage

        return amount

    def check_position(self):

        my_amount = float(self.pos["positionAmt"])

        if my_amount == 0:
            return False
        else:
            return True

    def enter_position(self):

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        bot = telegram.Bot(token="5459117011:AAG93i3Ls_t39R_c15QwAh2dGzMCqRGcalc")
        chat_id = 1667012769

        today_pos = random.randint(0, 1)

        if today_pos:
            self.exchange.create_market_buy_order(
                symbol = self.symbol,
                amount = self.__cal_amount()
            )

            print(now, "Long position successfully opened.")
            bot.sendMessage(chat_id, "Your Random Position is Long.")

            sleep(3)  # IDK why i shoud sleep 3sec but YouTube told me to do it

        elif not today_pos:
            self.exchange.create_market_sell_order(
                symbol = self.symbol,
                amount = self.__cal_amount()
            )

            print(now, "Short position successfully opended.")
            bot.sendMessage(chat_id, "Your Random Position is Short")

            sleep(3)

        self.__stoploss_setting(0.035 * int(self.pos['leverage']))

    def exit_position(self):

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        self.exchange.cancel_all_orders(self.symbol)

        amt = self.pos["positionAmt"]

        if amt > 0:
            self.exchange.create_market_sell_order(
                symbol = self.symbol,
                amount = amt,
                params = {"reduceOnly": True}
            )
        elif amt < 0:
            self.exchange.create_market_buy_order(
                symbol = self.symbol,
                amount = abs(amt),
                params={"reduceOnly": True}
            )
        print(now, "Position Successfully closed.")