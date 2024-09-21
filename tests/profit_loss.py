import pandas as pd

def calc_p_l(df):
    sell_price = 0
    buy_price = 0
    index = 0
    prev_sig = 1
    unique_sigs = 0
    profit_stream = {
        "time": [],
        "profit": []
    }
    profit = 0

    for sig in df["signal"]:
        if sig != prev_sig and sig != 0:
            if sig == 2:
                buy_price = df["Close"][index]
                prev_sig = 2
                index += 1
            elif sig == 1:
                sell_price = df["Close"][index]
                prev_sig = 1
                index += 1
            if unique_sigs % 2 == 0 and unique_sigs != 0:
                profit += 1000*(sell_price-buy_price)
                profit_stream["time"].append(df["time"][index])
                profit_stream["profit"].append(profit)
            unique_sigs += 1
            print(f"{sig}___{profit}")
    
    prof_stream = pd.DataFrame.from_dict(profit_stream)

    return profit, prof_stream





