import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# interval마다 랜덤 포지션 설정

df = pd.read_excel("eth_1hour_2y.xlsx")
df.set_index("datetime", inplace=True)

df["rate"] = round(df["close"] / df["open"], 4)
df["volatility"] = np.where(df["rate"] > 1, df["rate"], 2 - df["rate"])


# df["highup"] = round(df["high"] / df["open"], 4)
# df["downlow"] = round(df["low"] / df["open"], 4)

df["movement"] = np.where(df["rate"]>1, 1, 0)

par_list = list(df["movement"])

mathlist = []
for k in range(len(par_list)):
    mathlist.append((par_list[k-1], par_list[k]))

pnl_list = []
for j in mathlist:
    if j == (1, 0) or j == (0, 1):
        pnl_list.append(1)
    elif j == (1, 1) or j == (0, 0):
        pnl_list.append(0)

df["pnl"] = pnl_list

df['myRate'] = np.where(df["pnl"] == 1, df["volatility"], 2-df["volatility"])

df['myRate'] = np.where(df['myRate'] < 0.99, 0.99, df["myRate"])
df["myRate"] = df["myRate"] - 0.0008

ror_list = []
for i in range(len(df["myRate"])):
    ror_list.append(round(df["myRate"].cumprod()[i], 4))

plt.plot(df.index, ror_list)
plt.show()