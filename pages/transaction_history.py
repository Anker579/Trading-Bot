import streamlit as st
import pandas as pd
from trader import tran_hist
from main import make_trade

is_live = False
has_prompted = True

#my_auth = auth.authoriser()
#accID = my_auth.auth_deets(is_live, "id", has_prompted)
#access_token = my_auth.auth_deets(is_live, "token", has_prompted)

access_token = st.secrets["OANDA_ACCESS_TOKEN"]
accID = st.secrets["OANDA_ACCOUNT_ID"]

response_df = tran_hist.get_history(accID=accID, access_token=access_token)

order_fills = response_df.loc[
    response_df["type"] == "ORDER_FILL"
].copy()

order_fills["pl"] = order_fills["pl"].astype(float)

order_fills["time"] = (
    pd.to_datetime(order_fills["time"], utc=True)
    .dt.tz_convert("Europe/London")
)

display_data = order_fills.copy()

display_data["time"] = display_data["time"].dt.strftime(
    "%d/%m/%Y %H:%M"
)

realised_trades = order_fills.loc[
    order_fills["pl"] != 0
].copy()

realised_trades["Cumulative_profit"] = (
    realised_trades["pl"].cumsum()
)

hist_data = response_df[["time","pl", "type",]].copy()

hist_data.rename(columns={'time': 'Time', 'pl': 'Profit/Loss'}, inplace=True)

hist_data = hist_data.loc[hist_data["type"] == "ORDER_FILL"]

hist_data = hist_data.drop("type", axis=1)

hist_data = hist_data.loc[hist_data["Profit/Loss"] != "0.0000"]

hist_data['Profit/Loss'] = hist_data['Profit/Loss'].astype(float)

pl_list = hist_data["Profit/Loss"].to_list()

hist_data["Profit/Loss"] = pl_list

hist_data["Cumuluative_profit"] = hist_data["Profit/Loss"].cumsum()

st.title("TRANSACTION HISTORY")

st.write("This simply shows every trade made using the oanda account using the trading strategies discussed prior, It is around the start of August 2024 that the running algorithm was switched from the Comparator to the Simple Moving Average strategy and the impact on the profit is clear.")
st.write("The algorithm still struggles to maintain a consistent profit but this is to be expected with such a simplistic model, which does not stand a chance against the multi-million pound models that top Forex trading companies and banks use.")

show_data = st.checkbox("Show Database")
if show_data:
    st.write(
        display_data[
            [
                "time",
                "instrument",
                "units",
                "price",
                "pl",
                "reason"
            ]
        ]
    )

st.line_chart(
    data=realised_trades,
    x="time",
    y="Cumulative_profit"
)

if st.button("Click Here to Run the Trading Code (the app may not identify a buy/sell signal so nothing may happen)"):
    make_trade()