import datetime as dt
import yfinance as yf
import json
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from types import SimpleNamespace

# IMPORTANT changed DNS settings can effect this (will stop it working)
class api_connector():
    def __init__(self) -> None:
        self.period = 60
    
    def yf_get(self, period:int):
        x = dt.datetime.now()
        nowdate = f'{x.strftime("%Y")}-{x.strftime("%m")}-{x.strftime("%d")}'

        date_60_days_ago = x - dt.timedelta(days=(period-1))

        formatted_date = f"{date_60_days_ago.strftime('%Y')}-{date_60_days_ago.strftime('%m')}-{date_60_days_ago.strftime('%d')}"

        dataF = yf.download(
            "EURUSD=X",
            start=formatted_date,
            end=nowdate,
            interval='15m',
        )
        dataF.columns = dataF.columns.get_level_values(0)         
        return dataF


    def get_candles(self, is_live: bool, n: int, token, pair, interval):
        with open('./data/pair_mapping.json', 'r') as f:
            pair_mapping = json.load(f)
    
        if pair not in pair_mapping:
            raise ValueError(
                f"Invalid pair: {pair}. "
                f"Valid pairs are: {', '.join(pair_mapping.keys())}"
            )
    
        pair_const = pair_mapping[pair]
    
        client = API(
            access_token=token,
            environment="live" if is_live else "practice"
        )
    
        params = {
            "count": n,
            "granularity": "M15",
            "price": "B"
        }
    
        request = instruments.InstrumentsCandles(
            instrument=pair_const,
            params=params
        )
    
        response = client.request(request)
    
        candles = []
    
        for candle in response["candles"]:
            timestamp = int(
                dt.datetime.fromisoformat(
                    candle["time"].replace("Z", "+00:00")
                ).timestamp()
            )
    
            candles.append(
                SimpleNamespace(
                    time=timestamp,
                    bid=SimpleNamespace(
                        o=candle["bid"]["o"],
                        c=candle["bid"]["c"],
                        h=candle["bid"]["h"],
                        l=candle["bid"]["l"]
                    )
                )
            )
    
        return candles
