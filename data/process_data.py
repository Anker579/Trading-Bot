import pandas as pd
import json
import ta



class processor():
    def __init__(self) -> None:
        pass
    
    def check_pair(self, pair):
        with open('./data/pair_mapping.json', 'r') as f:
            pair_mapping = json.load(f)
        
        if pair not in pair_mapping:
            raise ValueError(f"Invalid pair: {pair}. Valid pairs are: {', '.join(pair_mapping.keys())}")
        
        pair_const = pair_mapping[pair]
        return pair_const

    def add_sma(self, df, sma_windows:list):
        #adds a column to input dataframe that is the running simple moving average for a given window
        for sma_window in sma_windows:
            df[f"sma_{sma_window}"] = ta.trend.SMAIndicator(close=df["Close"], window=sma_window).sma_indicator()
        return df
    
    def format_columns(self, candle_db):
        dfstream = pd.DataFrame(columns=['Open','Close','High','Low'])
        candles = candle_db
        i=0
        for candle in candles:
            dfstream.loc[i, ['Open']] = float(str(candle.bid.o))
            dfstream.loc[i, ['Close']] = float(str(candle.bid.c))
            dfstream.loc[i, ['High']] = float(str(candle.bid.h))
            dfstream.loc[i, ['Low']] = float(str(candle.bid.l))
            i=i+1

        dfstream['Open'] = dfstream['Open'].astype(float)
        dfstream['Close'] = dfstream['Close'].astype(float)
        dfstream['High'] = dfstream['High'].astype(float)
        dfstream['Low'] = dfstream['Low'].astype(float)

        return dfstream, candle