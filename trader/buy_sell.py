from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from oandapyV20.contrib.requests import MarketOrderRequest
import oandapyV20.endpoints.orders as orders

class trade():
    def __init__(self) -> None:
        pass
    
    def p_l_stops(self, dfstream, ratio, candle):
        SLTPRatio = ratio
        previous_candleR = abs(dfstream['High'].iloc[-2]-dfstream['Low'].iloc[-2])

        SLBuy = float(str(candle.bid.o))-previous_candleR
        SLSell = float(str(candle.bid.o))+previous_candleR

        TPBuy = float(str(candle.bid.o))+previous_candleR*SLTPRatio
        TPSell = float(str(candle.bid.o))-previous_candleR*SLTPRatio
        values = {"SLB": SLBuy,
                  "SLS": SLSell,
                  "TPB": TPBuy,
                  "TPS": TPSell
                  }
        return values
 
    def buy_sell(self, signal, client, accID, p_l_values):
        #BUY
        if signal == 1:
            mo = MarketOrderRequest(instrument="EUR_USD", units=-1000, takeProfitOnFill=TakeProfitDetails(price=p_l_values["TPS"]).data, stopLossOnFill=StopLossDetails(price=p_l_values["SLS"]).data)
            r = orders.OrderCreate(accountID = accID, data=mo.data)
            rv = client.request(r)
            print(rv)
        #SELL
        elif signal == 2:
            mo = MarketOrderRequest(instrument="EUR_USD", units=1000, takeProfitOnFill=TakeProfitDetails(price=p_l_values["TPB"]).data, stopLossOnFill=StopLossDetails(price=p_l_values["SLB"]).data)
            r = orders.OrderCreate(accountID = accID, data=mo.data)
            rv = client.request(r)
            print(rv)