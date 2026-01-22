


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
        #Gets passed the most recent row of the df and does simple calculations on the sma values
        df = df.iloc[-1]
        sma_50 = df.sma_50
        sma_200 = df.sma_200
        if sma_50 > sma_200:
            return 2
        #bullish
        elif sma_50 < sma_200:
            return 1
        #none
        else:
            return 0
        
