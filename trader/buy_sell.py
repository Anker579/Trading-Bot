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
 
    def buy_sell(self, signal, client, accID, p_l_values, pair):
        #SELL
        if signal == 1:
            print("SELL signal")
            mo = MarketOrderRequest(
                instrument=pair,
                units=-1000,
                takeProfitOnFill=TakeProfitDetails(
                    price=f'{p_l_values["TPS"]:.5f}'
                ).data,
                stopLossOnFill=StopLossDetails(
                    price=f'{p_l_values["SLS"]:.5f}'
                ).data
            )           
            r = orders.OrderCreate(accountID = accID, data=mo.data)
            rv = client.request(r)
            print(rv)
        #BUY
        elif signal == 2:
            print("BUY signal")
            mo = MarketOrderRequest(
                instrument=pair,
                units=1000,
                takeProfitOnFill=TakeProfitDetails(
                    price=f'{p_l_values["TPB"]:.5f}'
                ).data,
                stopLossOnFill=StopLossDetails(
                    price=f'{p_l_values["SLB"]:.5f}'
                ).data
            )
            r = orders.OrderCreate(accountID = accID, data=mo.data)
            rv = client.request(r)
            print(rv)
        else:
            print("No Trade signal")