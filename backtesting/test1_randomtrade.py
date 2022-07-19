import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

# interval마다 랜덤 포지션 설정

df = pd.read_excel("eth_1day_1y.xlsx")
df.set_index("datetime", inplace=True)

df["highup_loss"] = round(df["high"] / df["open"], 4)
df["highup_loss"] = df["randomRate"] = np.where(df["highup_loss"] >= 1, df["highup_loss"], df["highup_loss"])

df["downlow"] = round(df["low"] / df["open"], 4)

df["rate"] = round(df["close"] / df["open"], 4)
df["volatility"] = np.where(df["rate"] > 1, df["rate"], 2-df["rate"])


def randomRate(x):
    a = random.randint(0, 1)
    if a:
        rate = x
    else:
        rate = 2 - x

    return rate

df["randomRate"] = df["volatility"].apply(lambda x: randomRate(x))
df["randomRate"] = np.where(df["randomRate"] < 0.96, 0.96, df["randomRate"])
df["randomRate"] = df["randomRate"] - 0.0008


ro_list = []
for i in range(len(df["randomRate"])):
    ro_list.append(round(df["randomRate"].cumprod()[i], 4))


plt.plot(df.index, ro_list, "b.-")
plt.show()