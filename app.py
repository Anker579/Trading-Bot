import streamlit as st
import pandas as pd
from data import data_connector, process_data, signal_generators
from trader import auth, tran_hist
from tests.profit_loss import calc_p_l

st.set_page_config(
    page_title="Simple Algo Trader",
    page_icon="🤖",
)

st.title("Welcome To My Simple Forex Algorithmic Trader")

st.write("This is an app that uses given simple strategies to make decisions about whether to buy, sell or do nothing for a given foreign exchange pair.")
st.write(" It also allows you to use those strategies and evaluate how they would have performed on real data on historical data, i.e. backtesting the algorithm and seeing its performance.")

st.header("Algorithms")

st.subheader("Simple Moving Average")

st.write("This very common algorithm works by calculating two simple moving averages for the data, right now the given two are a 50 and 100 data point moving average, then, if the 50 day average has moved above the 200 day average it will return a buy signal, and vice versa for moving below.")
st.write("This means that this algorithm will only output a buy or sell signal, never a '0' or 'don't buy' signal, as such the model only makes a purchase each time the data pattern changes to a buy signal, not everytime there is a buy signal to prevent over-buying. This does however mean it takes less advantage of large upswings in a pairs performance, but ofcourse means less risk.")

st.subheader("Recent Open Comparator")


st.write("This algorithm instead only uses information about the last two candles (data point) to determine a buy, sell or nothing signal. It's method is best explained by an image showcasing the requirements for a buy or sell signal, shown below.")
col1, col2 = st.columns(2)
col1.image(image="Bearish.jpg", caption="BEARISH PATTERN (SELL SIGNAL)")
col2.image(image="Bullish.jpg", caption="BULLISH PATTERN (BUY SIGNAL)")
st.write("This algorithm therefore often returns a 0 or 'no action' signal, which is helpful to not always have a return and look for a specific behaviour, however, the behaviour this algorithm looks for can as easily occur due to approximately random fluctuations in a pairs value and therefore can make poor trades")
st.write("Algorithm Credit: [Code Training Youtube](%s)" % "https://www.youtube.com/watch?v=WcfKaZL4vpA&t=997s")

is_live = False
has_prompted = True

my_auth = auth.authoriser()
accID = my_auth.auth_deets(is_live, "id", has_prompted)
access_token = my_auth.auth_deets(is_live, "token", has_prompted)
my_sig_gens = signal_generators.sig_gens()


my_connector = data_connector.api_connector()
my_processor = process_data.processor()

back_data = my_connector.yf_get(period=60)

back_data = back_data.reset_index()

formatted_data = my_processor.add_sma(back_data, [50,200])

signal = []
signal.append(0)
for i in range(1,len(formatted_data)):
    df = formatted_data[i-1:i+1]
    signal.append(my_sig_gens.sma_sig_gen(df))

st.title("Backtesting predicted profit")

formatted_data["signal"] = signal

formatted_data

profit = calc_p_l(df=formatted_data)

#profit[0]
#profit[1]

backtest_profit = profit[1]

backtest_profit["cumulative profit"] = backtest_profit["profit"].cumsum()

backtest_profit

st.line_chart(data= backtest_profit,y="cumulative profit", x = "time")

#data = my_connector.yf_get(period=60)
#data = data.drop("High", axis=1)
#data = data.drop("Low", axis=1)
#data = data.drop("Volume", axis=1)
#data = data.drop("Adj Close", axis=1)
#data = data.drop("Open", axis=1)


#----------------------- GET AND SHOW TRANSACTION HISTORY ----------
st.title("TRANSACTION HISTORY")

response_df = tran_hist.get_history(accID=accID, access_token=access_token)

hist_data = response_df[["time","pl", "type",]].copy()

hist_data = hist_data.loc[hist_data["type"] == "ORDER_FILL"]

hist_data = hist_data.drop("type", axis=1)

hist_data = hist_data.loc[hist_data["pl"] != "0.0000"]

hist_data['pl'] = hist_data['pl'].astype(float)

pl_list = []

pl_list = hist_data["pl"].to_list()

hist_data["pl"] = pl_list

hist_data["cumuluative_profit"] = hist_data["pl"].cumsum()

hist_data

st.line_chart(data=hist_data, x="time", y="cumuluative_profit")

#print(hist_data)