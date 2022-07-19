import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import ccxt

token = "5456825419:AAGCl1GLksBdPQBk-fTpAw49f2PJxEu7DIM"
id = 1667012769

# 텔레그램 봇 객체 생성
bot = telegram.Bot(token)


# 바이낸스 객체 생성
binance = ccxt.binance()

# updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

def handler(update, context):
    user_text = update.message.text

    if user_text == "ETH" or user_text == "Eth" or user_text == "eth":
        eth = binance.fetch_ticker("ETH/USDT")
        cur_price = eth["last"]
        bot.sendMessage(id, "current ETH price : %f" %cur_price)

    elif user_text == "BTC" or user_text == "Btc" or user_text == "btc":
        btc = binance.fetch_ticker("BTC/USDT")
        cur_price = btc["last"]
        bot.sendMessage(id, "current BTC price : %f" %cur_price)





echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
