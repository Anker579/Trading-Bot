from data import data_connector, process_data, signal_generators
from trader import buy_sell
from oandapyV20 import API
from dotenv import load_dotenv
import os

load_dotenv()

def make_trade():
    is_live = False
    has_prompted = True

    my_trader = buy_sell.trade()

    access_token = os.getenv("OANDA_ACCESS_TOKEN")
    accID = os.getenv("OANDA_ACCOUNT_ID")

    if not access_token or not accID:
        raise RuntimeError("OANDA credentials not found in environment")

    my_connector = data_connector.api_connector()
    my_processor = process_data.processor()
    my_sig_gens = signal_generators.sig_gens()

    pair = my_processor.check_pair("EUR_USD")

    #my_candles = my_connector.get_candles(is_live, n=201, token=my_auth.auth_deets(is_live, "token", has_prompted), pair=pair, interval=1)
    my_candles = my_connector.get_candles(is_live, n=205, token=access_token, pair=pair, interval=1)


    #receives a tuple since the profit/loss calculator needs a candle - uses the one that format columns iterates over last
    format_tuple = my_processor.format_columns(my_candles)

    dfstream = format_tuple[0]

    candle = format_tuple[1]

    windows = [50,200]

    dfstream = my_processor.add_sma(dfstream, sma_windows=windows)

    # Ignore the newest potentially incomplete M15 candle
    completed_df = dfstream.iloc[:-1, :]

    signal = my_sig_gens.sma_sig_gen(completed_df)

    #Temp Debug Code
    print("\n--- SIGNAL DEBUG ---")
    print(completed_df[["Close", "sma_50", "sma_200"]].tail(3))
    print(f"Signal: {signal}")
    print("--------------------\n")

    # EXECUTING ORDERS

    #accID = my_auth.auth_deets(is_live, "id", has_prompted)
    #access_token = my_auth.auth_deets(is_live, "token", has_prompted)
    client = API(access_token)

    #-----------------------------------------------------------------
    # all this defines stop loss and stop profit     
    p_l_values = my_trader.p_l_stops(dfstream, 2., candle=candle)

    #print(dfstream.iloc[:-1,:])
    print(p_l_values)

    #my_trader.buy_sell(signal, client, accID, p_l_values, pair)
    print(f"DRY RUN - would execute signal: {signal}")

    #scheduler = BlockingScheduler()
    #scheduler.add_job(my_trader.buy_sell(signal, client, accID, p_l_values), 'cron', day_of_week='mon-fri', hour='00-23', minute='1,16,31,46', start_date='2022-01-12 12:00:00', timezone='America/Chicago')
    #scheduler.start()

if __name__ == "__main__":
    try:
        make_trade()
    except Exception as e:
        import traceback
        print("ERROR:", e)
        traceback.print_exc()
        raise
