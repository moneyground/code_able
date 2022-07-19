import pandas as pd
import numpy as np
import mpl_finance
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# SUPERTREND CALCULATION  ---수입산 코드; 작동원리 모름---
def get_supertrend(high, low, close, lookback, multiplier):
    # ATR

    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis=1, join='inner').max(axis=1)
    atr = tr.ewm(lookback).mean()

    # H/L AVG AND BASIC UPPER & LOWER BAND

    hl_avg = (high + low) / 2
    upper_band = (hl_avg + multiplier * atr).dropna()
    lower_band = (hl_avg - multiplier * atr).dropna()

    # FINAL UPPER BAND
    final_bands = pd.DataFrame(columns=['upper', 'lower'])
    final_bands.iloc[:, 0] = [x for x in upper_band - upper_band]
    final_bands.iloc[:, 1] = final_bands.iloc[:, 0]
    for i in range(len(final_bands)):
        if i == 0:
            final_bands.iloc[i, 0] = 0
        else:
            if (upper_band[i] < final_bands.iloc[i - 1, 0]) | (close[i - 1] > final_bands.iloc[i - 1, 0]):
                final_bands.iloc[i, 0] = upper_band[i]
            else:
                final_bands.iloc[i, 0] = final_bands.iloc[i - 1, 0]

    # FINAL LOWER BAND

    for i in range(len(final_bands)):
        if i == 0:
            final_bands.iloc[i, 1] = 0
        else:
            if (lower_band[i] > final_bands.iloc[i - 1, 1]) | (close[i - 1] < final_bands.iloc[i - 1, 1]):
                final_bands.iloc[i, 1] = lower_band[i]
            else:
                final_bands.iloc[i, 1] = final_bands.iloc[i - 1, 1]

    # SUPERTREND

    supertrend = pd.DataFrame(columns=[f'supertrend_{lookback}'])
    supertrend.iloc[:, 0] = [x for x in final_bands['upper'] - final_bands['upper']]

    for i in range(len(supertrend)):
        if i == 0:
            supertrend.iloc[i, 0] = 0
        elif supertrend.iloc[i - 1, 0] == final_bands.iloc[i - 1, 0] and close[i] < final_bands.iloc[i, 0]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
        elif supertrend.iloc[i - 1, 0] == final_bands.iloc[i - 1, 0] and close[i] > final_bands.iloc[i, 0]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
        elif supertrend.iloc[i - 1, 0] == final_bands.iloc[i - 1, 1] and close[i] > final_bands.iloc[i, 1]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
        elif supertrend.iloc[i - 1, 0] == final_bands.iloc[i - 1, 1] and close[i] < final_bands.iloc[i, 1]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 0]

    supertrend = supertrend.set_index(upper_band.index)
    supertrend = supertrend.dropna()[1:]

    # ST UPTREND/DOWNTREND

    upt = []
    dt = []
    close = close.iloc[len(close) - len(supertrend):]

    for i in range(len(supertrend)):
        if close[i] > supertrend.iloc[i, 0]:
            upt.append(supertrend.iloc[i, 0])
            dt.append(np.nan)
        elif close[i] < supertrend.iloc[i, 0]:
            upt.append(np.nan)
            dt.append(supertrend.iloc[i, 0])
        else:
            upt.append(np.nan)
            dt.append(np.nan)

    st, upt, dt = pd.Series(supertrend.iloc[:, 0]), pd.Series(upt), pd.Series(dt)
    upt.index, dt.index = supertrend.index, supertrend.index

    return st, upt, dt

# GET ENTRYPOINT ( State -> Stette)
def get_tse_entryPoint(prices, st, ema):
    stette = []
    mathlist = []
    long_list = [np.nan]
    short_list = [np.nan]
    entry_list = [np.nan]

    for i in range(len(st)):
        if prices[i] > ema[i] and prices[i] > st[i]:
            stette.append(1)

        elif (ema[i] < prices[i] < st[i]) or (ema[i] > prices[i] > st[i]):
            stette.append(0)

        elif prices[i] < ema[i] and prices[i] < st[i]:
            stette.append(-1)

    for k in range(len(stette)):
        mathlist.append((stette[k-1], stette[k]))

    stim = 0
    for p in mathlist:

        if p == (0, 1) or p == (-1, 1):
            long_list.append(prices[stim])
            short_list.append(np.nan)
            entry_list.append(prices[stim])
            stim = stim+1
        elif p == (0, -1) or p == (1, -1):
            long_list.append(np.nan)
            short_list.append(prices[stim])
            entry_list.append(prices[stim])
            stim = stim+1
        else:
            long_list.append(np.nan)
            short_list.append(np.nan)
            entry_list.append(np.nan)
            stim = stim+1

    long_list.pop()
    short_list.pop()
    entry_list.pop()

    return long_list, short_list, entry_list

# TakeProfit line
def get_takeprofit_line(price, supertrend, alpha):
    tp_line = []

    for i in range(len(price)):
        value = (1 + alpha * (1 - supertrend[i] / price[i])) * price[i]
        tp_line.append(value)

    return tp_line


# read data
filename = "eth_1day_1y.xlsx"

df = pd.read_excel(filename)
df.set_index("datetime", inplace=True)


# Setting Plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)


# Setting Index
day_list = []
name_list = []
for i, datetime in enumerate(df.index):
    if datetime.dayofweek == 0:
        day_list.append(i)
        name_list.append(datetime.strftime('%Y\n%m-%d'))

ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

# Candlestick Chart
mpl_finance.candlestick2_ohlc(ax, df['open'], df['high'], df['low'], df['close'], width=0.5, colorup='r', colordown='b')


plt.show()