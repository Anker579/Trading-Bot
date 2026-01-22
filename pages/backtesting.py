import streamlit as st
from data import data_connector, process_data, signal_generators
from tests.profit_loss import calc_p_l

my_sig_gens = signal_generators.sig_gens()
my_connector = data_connector.api_connector()
my_processor = process_data.processor()

back_data = my_connector.yf_get(period=60)

back_data = back_data.reset_index()

formatted_data = my_processor.add_sma(back_data, [50,200])


#--------------- adds signal to each transaction candle ------------------
signal = []
signal.append(0)
for i in range(1,len(formatted_data)):
    df = formatted_data[i-1:i+1]
    signal.append(my_sig_gens.sma_sig_gen(df))

formatted_data["signal"] = signal

profit = calc_p_l(df=formatted_data)

formatted_data = formatted_data.iloc[200:]

backtest_profit = profit[1]

backtest_profit["Cumulative profit"] = backtest_profit["profit"].cumsum()


st.title("Backtesting and backtest profit")

st.write("Backtesting is an essential part of trading with set strategies and even more so with algorithmic trading. As such here I have a simple but funtioning backtester which uses the Yahoo Finance api to retrieve the last 60 days of data for a given forex pair.")
st.write("My app achieves this by running the historical data through the buy/sell signal generators for each strategy, once this is done it can use a the stream of signals to calculate how much profit the algorithm/strategy would have made if it was trading live.")

f_data = st.checkbox("Display historical candles")
b_f_data = st.checkbox("Display profit stream for Backtest")

if f_data and b_f_data:
    col1, col2 = st.columns(2)
    col1.write(formatted_data)
    col2.write(backtest_profit)
elif f_data:
    formatted_data
elif b_f_data:
    backtest_profit

st.line_chart(data= backtest_profit,y="Cumulative profit", x = "time")