import datetime as dt
import yfinance as yf
from oanda_candles import Pair, Gran, CandleClient

# IMPORTANT changed DNS settings can effect this (will stop it working)
class api_connector():
    def __init__(self) -> None:
        self.period = 60
    
    def yf_get(self, period:int):
        x = dt.datetime.now()
        nowdate = f'{x.strftime("%Y")}-{x.strftime("%m")}-{x.strftime("%d")}'

        date_60_days_ago = x - dt.timedelta(days=(period-1))

        formatted_date = f"{date_60_days_ago.strftime('%Y')}-{date_60_days_ago.strftime('%m')}-{date_60_days_ago.strftime('%d')}"

        dataF = yf.download("EURUSD=X", start=formatted_date, end=nowdate, interval='15m')
        return dataF


    def get_candles(self, is_live:bool, n:int,token,pair,interval):
        client = CandleClient(token,real=is_live)

        pair_const = pair

        collector = client.get_collector(pair_const,Gran.M15)

        candles = collector.grab(n)
        return candles
