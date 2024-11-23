import streamlit as st
import pandas as pd
import hw
st.title("Formula-1 Events App")
st.markdown("In this app, the events that happen during a race is showed")
hw.main()  

data_path = "check.csv"
df = pd.read_csv(data_path)
df['date'] = pd.to_datetime(df['date'])

st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", value=df['date'].min())
end_date = st.sidebar.date_input("End Date", value=df['date'].max())
category_filter = st.sidebar.multiselect("Category", options=df["category"].unique(), default=df["category"].unique())
flag_filter = st.sidebar.multiselect("Flag", options=df["flag"].dropna().unique(), default=df["flag"].dropna().unique())
scope_filter = st.sidebar.multiselect("Scope", options=df["scope"].dropna().unique(), default=df["scope"].dropna().unique())

filtered_data = df[
    (df['date'] >= pd.Timestamp(start_date)) &
    (df['date'] <= pd.Timestamp(end_date)) &
    (df['category'].isin(category_filter)) &
    (df['flag'].isin(flag_filter)) &
    (df['scope'].isin(scope_filter))
]

st.header("Filtered Data")
st.write(filtered_data)
