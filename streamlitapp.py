import streamlit as st
import pandas as pd
import hw
st.title("Formula-1 Events App")
st.markdown("In this app, the events that happen during a race is showed")

data_path = "data.csv"
data = pd.read_csv(data_path)
data['date'] = pd.to_datetime(data['date'])

drivers_file = "F1_Drivers.csv"
drivers_data = pd.read_csv(drivers_file)

new_data = pd.merge(
    data, 
    drivers_data[['driver_number', 'name_acronym']],  
    on='driver_number', 
    how='left'
)

data['driver'] = new_data['name_acronym'] 

st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", value=data['date'].min())
end_date = st.sidebar.date_input("End Date", value=data['date'].max())
category_filter = st.sidebar.multiselect("Category", options=data["category"].unique(),default=data["category"].unique())
flag_filter = st.sidebar.multiselect("Flag", options=data["flag"].dropna().unique(),default=data["flag"].unique())
scope_filter = st.sidebar.multiselect("Scope", options=data["scope"].dropna().unique(),default=data["scope"].unique())

if st.sidebar.button("Apply Filters"):
    filtered_data = data[
        (data['date'] >= pd.Timestamp(start_date)) &
        (data['date'] <= pd.Timestamp(end_date)) &
        (data['category'].isin(category_filter) if category_filter else True) &
        (data['flag'].isin(flag_filter) if flag_filter else True) &
        (data['scope'].isin(scope_filter) if scope_filter else True)
    ]

    st.header("Filtered Events")
    st.write(filtered_data)
