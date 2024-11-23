import streamlit as st
import pandas as pd
import hw
st.title("Formula-1 Events App")
st.markdown("In this app, the events that happen during a race is showed")

data_file = "data.csv"
data = pd.read_csv(data_file)
data['date'] = pd.to_datetime(data['date'])

data['flag'] = data['flag'].fillna('None')
data['scope'] = data['scope'].fillna('None')

drivers_file = "F1_Drivers.csv"
drivers_data = pd.read_csv(drivers_file)

new_data = pd.merge(
    data, 
    drivers_data[['driver_number', 'name_acronym']],  
    on='driver_number', 
    how='left'
)

new_data['driver'] = new_data['name_acronym'] 
new_data.drop(columns=['name_acronym'],inplace=True)
st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", value=new_data['date'].min())
end_date = st.sidebar.date_input("End Date", value=new_data['date'].max())
category_filter = st.sidebar.multiselect("Category", options=new_data["category"].unique(),default=new_data["category"].unique())
flag_filter = st.sidebar.multiselect("Flag", options=new_data["flag"].dropna().unique(),default=new_data["flag"].unique())
scope_filter = st.sidebar.multiselect("Scope", options=new_data["scope"].dropna().unique(),default=new_data["scope"].unique())

if st.sidebar.button("Apply Filters"):
    filtered_data = new_data[
        (new_data['date'] >= pd.Timestamp(start_date)) &
        (new_data['date'] <= pd.Timestamp(end_date)) &
        (new_data['category'].isin(category_filter) if category_filter else True) &
        (new_data['flag'].isin(flag_filter) if flag_filter else True) &
        (new_data['scope'].isin(scope_filter) if scope_filter else True)
    ]
    data_wo_dn = filtered_data.drop(columns=['driver_number'])
    for idx, row in data_wo_dn.iterrows():
        if pd.notna(row['driver']):
            driver_link = f"[{row['driver']}](/?driver={row['driver']})"  
        else:
            driver_link = "None"
        data_wo_dn.at[idx, 'driver'] = driver_link

query_params = st.query_params
selected_driver = query_params.get("driver", [None])[0]

if selected_driver:
    driver_info = drivers_data[drivers_data['name_acronym'] == selected_driver]
    
    if not driver_info.empty:
        st.header(f"Driver Information: {selected_driver}")
        st.write(f"### Name: {driver_info['full_name'].iloc[0]}")
        st.write(f"### Driver Number: {driver_info['driver_number'].iloc[0]}") 
        st.write(f"### Team:{driver_info['team_name'].iloc[0]}")
        st.write(f"### Nation:{driver_info['country_code'].iloc[0]}")
