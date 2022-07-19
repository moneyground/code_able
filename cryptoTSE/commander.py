import pandas as pd
import indicators
from math import floor
import telegram


class moneyGoose:
    def __init__(self, exchange, symbol, interval):
        self.exchange = exchange
        self.symbol = symbol

        data = self.exchange.fetch_ohlcv(
            symbol=self.symbol,
            timeframe=interval,
            since=None,
            limit=201
        )

        # transfer historical data into DataFrame object
        df = pd.DataFrame(
            data=data,
            columns=["datetime", "open", "high", "low", "close", "volume"]
        )

        df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")
        df.set_index("datetime", inplace=True)

        df["ema200"] = indicators.get_ema(df["close"], 200)

        df["supertrend"] = indicators.get_supertrend(df["high"], df["low"], df["close"],
                                                      lookback=10, multiplier=3)

        self.df = df

        position = self.exchange.fetch_balance()['info']['positions']
        pos = [p for p in position if p['symbol'] == self.symbol.replace("/", "")][0]

        self.pos = pos

    def __tp_sl_setting(self, pnlRatio):

        stopPrice = self.df["supertrend"][-1]


        amount = 0
        entryPrice = 0

        if self.pos["symbol"] == self.symbol.replace("/", ""):
            entryPrice = float(self.pos["entryPrice"])
            amount = float(self.pos["positionAmt"])

        side = ""

        # side
        if amount > 0:
            side = "sell"
        elif amount < 0:
            side = "buy"

        takePrice = (1 + pnlRatio * (1 - stopPrice / entryPrice)) * entryPrice


        params_tp = {
            'stopPrice': takePrice,
            'closePosition': True
        }

        params_sl = {
            'stopPrice': stopPrice,
            'closePosition': True
        }

        self.exchange.create_order(self.symbol, "TAKE_PROFIT_MARKET", side, abs(amount), takePrice, params_tp)
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

    def get_entryPoint(self):

        def confirm(datum):
            if datum["open"] > datum["ema200"] and datum["open"] > datum["supertrend"]:
                return 1
            elif datum["open"] < datum["ema200"] and datum["open"] < datum["supertrend"]:
                return -1
            else:
                return 0

        past_10m = self.df.iloc[-3]
        past_5m = self.df.iloc[-2]
        present = self.df.iloc[-1]

        res = [confirm(past_10m), confirm(past_5m), confirm(present)]
        res = tuple(res)

        if res == (0, 1, 1) or res == (-1, 1, 1):
            return 1
        elif res == (0, -1, -1) or res ==(1, -1, -1):
            return -1
        else:
            return 0

    def enter_position(self, PnLratio):

        bot = telegram.Bot(token="5459117011:AAG93i3Ls_t39R_c15QwAh2dGzMCqRGcalc")
        chat_id = 1667012769

        if self.get_entryPoint() == 1:
            # enter position
            self.exchange.create_market_buy_order(self.symbol, self.__cal_amount())

            # tp/sl setting
            self.__tp_sl_setting(PnLratio)

            # sendMessage
            bot.sendMessage(chat_id, "Long position entered")

        elif self.get_entryPoint() == -1:

            # enter position
            self.exchange.create_market_sell_order(self.symbol, self.__cal_amount())

            # tp/sl setting
            self.__tp_sl_setting(PnLratio)

            # sendMessage
            bot.sendMessage(chat_id, "Short position entered")