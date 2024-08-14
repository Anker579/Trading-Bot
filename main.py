from data import data_connector, process_data, signal_generators
from apscheduler.schedulers.blocking import BlockingScheduler
from trader import auth, buy_sell
from oandapyV20 import API

is_live = False
has_prompted = False

my_trader = buy_sell.trade()
my_auth = auth.authoriser()
my_connector = data_connector.api_connector()
my_processor = process_data.processor()
my_sig_gens = signal_generators.sig_gens()

my_candles = my_connector.get_candles(False, 3, token=my_auth.auth_deets(is_live, "token"), pair="EUR_USD", interval=1)

#receives a tuple since the profit/loss calculator needs a candle - uses the one that format columns iterates over last
format_tuple = my_processor.format_columns(my_candles)

dfstream = format_tuple[0]

windows = [50,200]

dfstream = my_processor.add_sma(dfstream, sma_windows=windows)

candle = format_tuple[1]

#signal = my_sig_gens.og_sig_gen(dfstream.iloc[:-1,:])
signal = my_sig_gens.sma_sig_gen(dfstream.iloc[:-1,:])

# EXECUTING ORDERS

accID = my_auth.auth_deets(is_live, "id")
access_token = my_auth.auth_deets(is_live, "token")
client = API(access_token)

#-----------------------------------------------------------------
# all this defines stop loss and stop profit     
p_l_values = my_trader.p_l_stops(dfstream, 2., candle=candle)
    
print(dfstream.iloc[:-1,:])
print(p_l_values)
    
my_trader.buy_sell(signal, client, accID, p_l_values)

#scheduler = BlockingScheduler()
#scheduler.add_job(my_trader.buy_sell(signal, client, accID, p_l_values), 'cron', day_of_week='mon-fri', hour='00-23', minute='1,16,31,46', start_date='2022-01-12 12:00:00', timezone='America/Chicago')
#scheduler.start()