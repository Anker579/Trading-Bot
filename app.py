import streamlit as st
import pandas as pd
from data import data_connector, process_data
from trader import auth, tran_hist

is_live = False
has_prompted = True

my_auth = auth.authoriser()
accID = my_auth.auth_deets(is_live, "id", has_prompted)
access_token = my_auth.auth_deets(is_live, "token", has_prompted)


my_connector = data_connector.api_connector()
my_processor = process_data.processor()

data = my_connector.yf_get(period=60)
data = data.drop("High", axis=1)
data = data.drop("Low", axis=1)
data = data.drop("Volume", axis=1)
data = data.drop("Adj Close", axis=1)
data = data.drop("Open", axis=1)

st.title("Hello World")


response_df = tran_hist.get_history(accID=accID, access_token=access_token)

hist_data = response_df[["time","pl", "type",]].copy()

hist_data = hist_data.loc[hist_data["type"] == "ORDER_FILL"]

hist_data

st.line_chart(data=hist_data, x="time", y="pl")

print(response_df)