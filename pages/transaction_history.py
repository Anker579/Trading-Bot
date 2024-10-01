import streamlit as st
from trader import tran_hist, #auth
from main import make_trade

is_live = False
has_prompted = True

#my_auth = auth.authoriser()
#accID = my_auth.auth_deets(is_live, "id", has_prompted)
#access_token = my_auth.auth_deets(is_live, "token", has_prompted)
access_token='eac0b37f2067f37b1bb9884dfb473e6b-e204948541e0c8a2ba8a967492225ca7'
accID = '101-004-29576199-001'

response_df = tran_hist.get_history(accID=accID, access_token=access_token)

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

st.write("This simply shows every trade made using the oanda account using the trading strategies discussed prior, It is aroung the start of August 2024 that the running algorithm was switched from the Comparator to the Simple Moving Average strategy and the impact on the profit is clear.")
st.write("The algorithm still struggles to maintain a consistent profit but this is to be expected with such a simplistic model, which does not stand a chance against the multi-million pound models that top Forex trading companies and banks use.")

show_data = st.checkbox("Show Database")
if show_data:
    hist_data

st.line_chart(data=hist_data, x="Time", y="Cumuluative_profit")

if st.button("Click Here to Make a Trade on the EUR/USD Pair that uses the SMA Algorithm"):
    make_trade()