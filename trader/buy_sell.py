from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from oandapyV20.contrib.requests import MarketOrderRequest
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
import config

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
        # get position details to know if the trade is already open or not
        position_request = positions.PositionDetails(
            accountID=accID,
            instrument=pair
        )

        position = client.request(position_request)["position"]

        long_units = float(position["long"]["units"])
        short_units = float(position["short"]["units"])

        #SELL
        if signal == 1:
            print("SELL signal")
            if short_units < 0:
                print("Already short - no new order")
                return False

            if long_units > 0:
                close_request = positions.PositionClose(
                    accountID=accID,
                    instrument=pair,
                    data={"longUnits": "ALL"}
                )
                client.request(close_request)
                print("Closed existing long position")

            mo = MarketOrderRequest(
                instrument=pair,
                units= (-1 * config.TRADE_UNITS),
                takeProfitOnFill=TakeProfitDetails(
                    price=f'{p_l_values["TPS"]:.5f}'
                ).data,
                stopLossOnFill=StopLossDetails(
                    price=f'{p_l_values["SLS"]:.5f}'
                ).data
            )           
            r = orders.OrderCreate(accountID = accID, data=mo.data)
            print(client.request(r))
            return True
        
        #BUY
        elif signal == 2:
            print("BUY signal")

            if long_units > 0:
                print("Already long - no new order")
                return False

            if short_units < 0:
                close_request = positions.PositionClose(
                    accountID=accID,
                    instrument=pair,
                    data={"shortUnits": "ALL"}
                )
                client.request(close_request)
                print("Closed existing short position")

            mo = MarketOrderRequest(
                instrument=pair,
                units=config.TRADE_UNITS,
                takeProfitOnFill=TakeProfitDetails(
                    price=f'{p_l_values["TPB"]:.5f}'
                ).data,
                stopLossOnFill=StopLossDetails(
                    price=f'{p_l_values["SLB"]:.5f}'
                ).data
            )
            r = orders.OrderCreate(accountID = accID, data=mo.data)
            print(client.request(r))
            return True

        else:
            print("No Trade signal")