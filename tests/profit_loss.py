class p_l():

    def __init__(self) -> None:
        pass
        
    def calc_p_l(self, df):
        sell_price = 0
        buy_price = 0
        index = 0 
        pair_transactions = {
            "buy":0,
            "sell":0
        }
        profit = 0
        for s in df["signal"]:
            print(s)
            if s == 2:
                buy_price = df["Close"][index]
                pair_transactions["buy"] += 1
            elif s == 1:
                sell_price = df["Close"][index]
                pair_transactions["sell"] += 1
            index += 1
        return profit