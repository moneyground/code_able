# -*- coding: utf-8 -*-

import ccxt
import datetime
import time
import commander
import telegram


bot = telegram.Bot(token = "5459117011:AAG93i3Ls_t39R_c15QwAh2dGzMCqRGcalc")
chat_id = 1667012769



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

# my TradingSymbol
symbol = "ETH/USDT"
interval = "1h"

print("Starting Program...")

while True:
    now = datetime.datetime.now()

    if now.minute == 0 and 1 <= now.second < 2:

        General = commander.moneyGoose(binance, symbol, interval)

        if General.get_entryPoint() == 1 and not General.check_position():
            bot.sendMessage(chat_id, "Long position recommended")
            print("Long")
        elif General.get_entryPoint() == -1 and not General.check_position():
            bot.sendMessage(chat_id, "Short position recommended")
            print("Short")
        else:
            pass


        time.sleep(1)