import datetime as dt
import yfinance as yf


class yf_connector():
    def __init__(self) -> None:
        self.period = 60
    
    def yf_get(self):
        x = dt.datetime.now()
        nowdate = f'{x.strftime("%Y")}-{x.strftime("%m")}-{x.strftime("%d")}'

        date_60_days_ago = x - dt.timedelta(days=(59))

        formatted_date = f"{date_60_days_ago.strftime('%Y')}-{date_60_days_ago.strftime('%m')}-{date_60_days_ago.strftime('%d')}"

        dataF = yf.download("EURUSD=X", start=formatted_date, end=nowdate, interval='15m')
        return dataF


