import pandas as pd

def calc_p_l(df):
    sell_price = 0
    buy_price = 0
    index = 0
    prev_sig = 1
    unique_sigs = 1
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
                #print(buy_price, index, "s")
            elif sig == 1:
                sell_price = df["Close"][index]
                #print(sell_price, index, "b")
                prev_sig = 1
            if unique_sigs % 2 == 0 and unique_sigs != 0:
                #print(buy_price, sell_price)
                #print(1000*(sell_price-buy_price)) 
                #print(index)
                #print(df["Datetime"][index])
                
                profit = 1000*(sell_price-buy_price)
                profit_stream["time"].append(df["Datetime"][index])
                profit_stream["profit"].append(profit)
            unique_sigs += 1
            #print(f"{sig}___{profit}")
        index += 1
    
    prof_stream = pd.DataFrame.from_dict(profit_stream)

    return profit, prof_stream





