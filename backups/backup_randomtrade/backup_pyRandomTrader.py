# -*- coding: utf-8 -*-

import ccxt
import datetime
import telegram
import nobrain

bot = telegram.Bot(token= "")
chat_id = None

with open("Binance_API_key.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()


# create binance object
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

# Checking Balance
balance = binance.fetch_balance()
usdt = balance["total"]["USDT"]

symbol = "ETH/USDT"

position = {
    "type" : None,
    "amount" : 0
}

while True:
    now = datetime.datetime.now()

    if now.hour == 8 and now.minute == 50 and (0 <= now.second < 10):
        noBrain.exit_position(binance, symbol, position)
        position["type"] = 0
        position["amount"] = 0

    if now.hour == 9 and now.minute == 00 and (20 <= now.second < 30):

        # 1. Calculate Amount
        coin = binance.fetch_ticker(symbol=symbol)
        cur_price = coin["last"]
        amount = noBrain.cal_amount(symbol, usdt, cur_price, 1, 3)

        # 2. Enter Position
        noBrain.enter_position(binance, symbol, cur_price, amount, position, None, 0.97)