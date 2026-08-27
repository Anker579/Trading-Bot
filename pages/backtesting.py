import streamlit as st
import pandas as pd
from data import data_connector, process_data
from backtest import run_sma_backtest
import config

my_connector = data_connector.api_connector()

period = config.BACKTEST_PERIOD

sma_windows = config.SMA_WINDOWS

@st.cache_data(ttl=900)
def load_backtest_data():

    token = st.secrets["OANDA_ACCESS_TOKEN"]

    connector = data_connector.api_connector()
    processor = process_data.processor()

    candles = connector.get_candles(
        is_live=config.OANDA_ENVIRONMENT == "live",
        n=5000,
        token=token,
        pair=config.PAIR,
        interval=config.TIMEFRAME
    )

    data, _ = processor.format_columns(candles)

    # Backtester expects Date or Datetime
    data = data.rename(columns={"Time": "Datetime"})

    data["Datetime"] = pd.to_datetime(
        data["Datetime"],
        unit="s",
        utc=True
    )

    # Keep approximately the requested backtest period
    cutoff = (
        pd.Timestamp.now(tz="GMT")
        - pd.Timedelta(days=config.BACKTEST_PERIOD)
    )

    data = data[data["Datetime"] >= cutoff]

    return data.reset_index(drop=True)


try:
    back_data = load_backtest_data()
except Exception as e:
    st.error(f"Failed to retrieve OANDA data: {e}")
    st.stop()

st.title("Backtesting and backtest profit")

st.subheader("Strategies")

use_crossover = st.checkbox(
    "SMA crossover - exit on opposite crossover",
    value=True
)

use_sltp = st.checkbox(
    "SMA crossover - stop loss / take profit",
    value=True
)

if not use_crossover and not use_sltp:
    st.info("Select at least one strategy to run the backtest.")
    st.stop()

results = {}
formatted_data = None

if use_crossover:
    crossover_data, crossover_profit, crossover_metrics = run_sma_backtest(
        back_data,
        config.SMA_WINDOWS,
        exit_strategy="crossover"
    )

    crossover_profit["Cumulative profit"] = (
        crossover_profit["profit"].cumsum()
    )

    results["SMA Crossover"] = {
        "profit": crossover_profit,
        "metrics": crossover_metrics
    }

    formatted_data = crossover_data

if use_sltp:
    sltp_data, sltp_profit, sltp_metrics = run_sma_backtest(
        back_data,
        config.SMA_WINDOWS,
        exit_strategy="sltp",
        sl_tp_ratio=config.SL_TP_RATIO,
        trade_units=config.TRADE_UNITS
    )

    sltp_profit["Cumulative profit"] = (
        sltp_profit["profit"].cumsum()
    )

    results["SMA + SL/TP"] = {
        "profit": sltp_profit,
        "metrics": sltp_metrics
    }

    if formatted_data is None:
        formatted_data = sltp_data

for strategy_name, result in results.items():
    st.subheader(strategy_name)

    metrics = result["metrics"]

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

st.write(f"Backtesting is an essential part of trading with set strategies and even more so with algorithmic trading. As such here I have a simple but funtioning backtester which uses the same Oanda API to retrieve the last {config.BACKTEST_PERIOD} days of data for a given forex pair.")
st.write("My app achieves this by running the historical data through the buy/sell signal generators for each strategy, once this is done it can use a the stream of signals to calculate how much profit the algorithm/strategy would have made if it was trading live.")



chart_series = []

for strategy_name, result in results.items():
    profit_stream = result["profit"]

    if profit_stream.empty:
        continue

    series = (
        profit_stream
        .set_index("time")["Cumulative profit"]
        .rename(strategy_name)
    )

    chart_series.append(series)

if chart_series:
    comparison_chart = pd.concat(
        chart_series,
        axis=1
    ).sort_index()

    comparison_chart = comparison_chart.ffill().fillna(0)

    st.subheader("Cumulative profit comparison")
    st.line_chart(comparison_chart)
else:
    st.info("No completed trades were generated.")

f_data = st.checkbox("Display historical candles")

b_f_data = st.checkbox("Display backtest trades")

if f_data:
    st.subheader("Historical candles")
    st.write(formatted_data)

if b_f_data:
    for strategy_name, result in results.items():
        st.subheader(f"{strategy_name} trades")
        st.write(result["profit"])