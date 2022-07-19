import pyupbit
import time
import datetime
import telegram

bot = telegram.Bot(token="5542018705:AAG59zDLDgFuJjesRyJNMkVlx1al4zKE-DA")
chat_id = 1667012769

tickers = pyupbit.get_tickers(fiat="KRW")
op_mode = False

print("Starting Program....")

while True:
    now = datetime.datetime.now()

    if not now.minute%5 and (5 < now.second < 7):
        op_mode = True
    else:
        op_mode = False

    if op_mode:

        for ticker in tickers:
            df = pyupbit.get_ohlcv(ticker, interval="minute5", count = 38)
            df["vma"] = df["volume"].rolling(window=36).mean().shift(1)

            past = df.iloc[-2]
            present = df.iloc[-1]

            if present["volume"] > present["vma"]*10 and past["close"] < present["open"]:
                bot.sendMessage(chat_id, "%s's volume is going skyrocket!" %ticker)
                print("Nuclear launch Detected on %s" %ticker)

            time.sleep(0.1)