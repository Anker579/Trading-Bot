import pandas as pd


class sig_gens():
    
    def __init__(self) -> None:
        pass

    def og_sig_gen(self, df):
        #is passed the last two rows of the df to calculate signals
        open = df.Open.iloc[-1]
        close = df.Close.iloc[-1]
        previous_open = df.Open.iloc[-2]
        previous_close = df.Close.iloc[-2]
        # Bearish Pattern
        if (open>close and 
        previous_open<previous_close and 
        close<previous_open and
        open>=previous_close):
            return 1
        # Bullish Pattern
        elif (open<close and 
            previous_open>previous_close and 
            close>previous_open and
            open<=previous_close):
            return 2
        # No clear pattern
        else:
            return 0

    def sma_sig_gen(self, df):
        # Calculates if the SMA50 and SMA200 have crossed over in the last two rows of the dataframe
        previous = df.iloc[-2]
        current = df.iloc[-1]

        values = [
            previous.sma_50,
            previous.sma_200,
            current.sma_50,
            current.sma_200
        ]

        if any(pd.isna(value) for value in values):
            return 0

        # Bullish crossover: SMA50 moves from below SMA200 to above it
        if (
            previous.sma_50 <= previous.sma_200
            and current.sma_50 > current.sma_200
        ):
            return 2

        # Bearish crossover: SMA50 moves from above SMA200 to below it
        elif (
            previous.sma_50 >= previous.sma_200
            and current.sma_50 < current.sma_200
        ):
            return 1

        # No crossover
        else:
            return 0
