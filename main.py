from data import data_connector, process_data, signal_generators
from trader import buy_sell
from oandapyV20 import API
from dotenv import load_dotenv
import config
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

LAST_TRADE_FILE = os.path.join(BASE_DIR, ".last_trade_candle")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

def make_trade():
    is_live = config.OANDA_ENVIRONMENT == "live"

    my_trader = buy_sell.trade()

    access_token = os.getenv("OANDA_ACCESS_TOKEN")
    accID = os.getenv("OANDA_ACCOUNT_ID")

    if not access_token or not accID:
        raise RuntimeError("OANDA credentials not found in environment")

    my_connector = data_connector.api_connector()
    my_processor = process_data.processor()
    my_sig_gens = signal_generators.sig_gens()

    pair = my_processor.check_pair(config.PAIR)

    my_candles = my_connector.get_candles(
        is_live,
        n=config.CANDLE_COUNT,
        token=access_token,
        pair=pair,
        interval=config.TIMEFRAME
    )

    #receives a tuple since the profit/loss calculator needs a candle - uses the one that format columns iterates over last
    format_tuple = my_processor.format_columns(my_candles)

    dfstream = format_tuple[0]

    candle = format_tuple[1]

    dfstream = my_processor.add_sma(
        dfstream,
        sma_windows=config.SMA_WINDOWS
    )

    # Ignore the newest potentially incomplete M15 candle
    completed_df = dfstream.iloc[:-1, :]

    signal = my_sig_gens.sma_sig_gen(
        completed_df,
        config.SMA_WINDOWS,
        )

    # Identify the completed M15 candle that generated this signal
    candle_id = str(int(completed_df["Time"].iloc[-1]))
    
    last_trade_candle = None
    # Adds execution signal logic to prevent duplicate trades for the same candle
    if os.path.exists(LAST_TRADE_FILE):
        with open(LAST_TRADE_FILE, "r") as f:
            last_trade_candle = f.read().strip()
    
    if signal != 0 and candle_id == last_trade_candle:
        print(f"Signal already processed for candle {candle_id}")
        execution_signal = 0
    else:
        execution_signal = signal

    # Debug Code
    print("\n--- SIGNAL DEBUG ---")
    print(
        completed_df[
            [
                "Close",
                f"sma_{config.SMA_WINDOWS[0]}",
                f"sma_{config.SMA_WINDOWS[1]}"
            ]
        ].tail(3)
        )
    print(f"Signal: {signal}")
    print(f"Execution signal: {execution_signal}")
    print(f"Candle ID: {candle_id}")
    print(f"Dry run: {DRY_RUN}")
    print("--------------------\n")
    
    # EXECUTING ORDERS

    #accID = my_auth.auth_deets(is_live, "id", has_prompted)
    #access_token = my_auth.auth_deets(is_live, "token", has_prompted)
    client = API(
        access_token=access_token,
        environment=config.OANDA_ENVIRONMENT
    )

    #-----------------------------------------------------------------
    # all this defines stop loss and stop profit     
    p_l_values = my_trader.p_l_stops(
        dfstream,
        config.SL_TP_RATIO,
        candle=candle
    )

    if execution_signal == 0:
        print("No trade to execute")

    elif DRY_RUN:
        print(f"DRY RUN - would execute signal: {execution_signal}")

    else:
        trade_made = my_trader.buy_sell(
            execution_signal,
            client,
            accID,
            p_l_values,
            pair
        )

        # Only mark the candle as processed after the OANDA order succeeds and has traded
        if trade_made:
            with open(LAST_TRADE_FILE, "w") as f:
                f.write(candle_id)
    
            print(f"------ TRADE MADE - code: {execution_signal} --------")
            print(f"Recorded traded candle: {candle_id}")

if __name__ == "__main__":
    try:
        make_trade()
    except Exception as e:
        import traceback
        print("ERROR:", e)
        traceback.print_exc()
        raise