# -*- coding: utf-8 -*-

import ccxt
import datetime
import telegram
import noBrain
import time

bot = telegram.Bot(token= "5453595066:AAHcYjB3wXgykiYCL-jHSrGSvMn8djOXgqw")
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

# Checking Balance
balance = binance.fetch_balance()
usdt = balance["total"]["USDT"]

symbol = "ETH/USDT" # input("Enter the symbol that u want to trade. : ")

op_mode = False

print("System Running.....")

while True:
    now = datetime.datetime.now()

    if op_mode and now.hour == 8 and now.minute == 50 and (0 <= now.second < 10):

        # Exit Position
        noBrain.exit_position(binance, symbol, now)
        time.sleep(10)

    if now.hour == 9 and now.minute == 00 and (20 <= now.second < 30):

        op_mode = True

        # 1. Updating myBalance
        balance = binance.fetch_balance()
        usdt = balance["total"]["USDT"]

        # 2. Calculate Amount
        coin = binance.fetch_ticker(symbol=symbol)
        cur_price = coin["last"]

        position = binance.fetch_balance()['info']['positions']
        pos = [p for p in position if p['symbol'] == symbol.replace("/", "")][0]

        leverage = int(pos['leverage'])

        cutRate = 0.04 * leverage

        amount = round(noBrain.cal_amount(symbol, usdt, cur_price, 1, leverage), 4)

        # 3. Enter Position
        noBrain.enter_position(binance, symbol, cur_price, amount, None, cutRate, now)

        time.sleep(10)