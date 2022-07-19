# -*- coding: utf-8 -*-

import ccxt
import datetime
import time
import commander


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

    if now.minute == 0 and 5 <= now.second < 6:

        General = commander.moneyGoose(binance, symbol, interval)

        if General.get_entryPoint() and not General.check_position():
            General.enter_position(3)
        else:
            pass

        time.sleep(1)