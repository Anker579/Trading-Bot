import streamlit as st
from data import data_connector
from backtest import run_sma_backtest
import config

my_connector = data_connector.api_connector()

period = config.BACKTEST_PERIOD

sma_windows = config.SMA_WINDOWS

back_data = my_connector.yf_get(
    period=config.BACKTEST_PERIOD,
    ticker=config.YF_TICKER,
    interval=config.YF_INTERVAL
    )

formatted_data, backtest_profit, metrics = run_sma_backtest(
    back_data,
    config.SMA_WINDOWS
)

backtest_profit["Cumulative profit"] = backtest_profit["profit"].cumsum()

st.title("Backtesting and backtest profit")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Profit",
    f"{metrics['total_profit']:.2f}"
)

col2.metric(
    "Trades",
    metrics["number_of_trades"]
)

col3.metric(
    "Win Rate",
    f"{metrics['win_rate']:.1f}%"
)

col4.metric(
    "Max Drawdown",
    f"{metrics['max_drawdown']:.2f}"
)

st.write(f"Backtesting is an essential part of trading with set strategies and even more so with algorithmic trading. As such here I have a simple but funtioning backtester which uses the Yahoo Finance api to retrieve the last {config.BACKTEST_PERIOD} days of data for a given forex pair.")
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