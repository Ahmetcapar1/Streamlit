import streamlit as st
import pandas as pd
import hw
st.title("Formula-1 Events App")
st.markdown("In this app, the events that happen during a race is showed")

data_path = "check.csv"
data = pd.read_csv(data_path)
data['date'] = pd.to_datetime(data['date'])

st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", value=data['date'].min())
end_date = st.sidebar.date_input("End Date", value=data['date'].max())
category_filter = st.sidebar.multiselect("Category", options=data["category"].unique())
scope_filter = st.sidebar.multiselect("Scope", options=data["scope"].dropna().unique())

filtered_data = data[
    (data['date'] >= pd.Timestamp(start_date)) &
    (data['date'] <= pd.Timestamp(end_date)) &
    (data['category'].isin(category_filter)) &
    (data['scope'].isin(scope_filter))
]

st.header("Events")
st.write(filtered_data)
