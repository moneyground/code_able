import ccxt
import pandas as pd
from pprint import pprint
import time


api_key = "gbE8gc7uhm3OX8OjtIey6vTZMDu7B7r9bjPT9LHfJvJXm0gpJtygdrbcsAXB4VEF"
secret = "3LUseqgQOAWfU4YllbC85OQoxvz3NgO9uT7tlcSDqpkxvUxxs2QaZaYCgMfz3g9s"

# create binance object
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

symbol = "ETH/USDT"

data = binance.fetch_ohlcv(
    symbol=symbol,
    timeframe="5m",
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

position = binance.fetch_balance()['info']['positions']
pos = [p for p in position if p['symbol'] == "ETHUSDT"][0]

pprint(pos)

takePrice = 1389.52
stopPrice = 1346.54


params_tp = {
    'stopPrice': takePrice,
    'closePosition': True
}

params_sl = {
    'stopPrice': stopPrice,
    'closePosition': True
}

