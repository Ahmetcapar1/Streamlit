import streamlit as st
import pandas as pd
import hw

st.set_page_config(page_title="Formula-1 Events App", layout="wide")

# Load data
data_file = "data.csv"
data = pd.read_csv(data_file)
data['date'] = pd.to_datetime(data['date'])

# Fill NaN values for flag and scope
data['flag'] = data['flag'].fillna('None')
data['scope'] = data['scope'].fillna('None')

# Load driver data
drivers_file = "F1_Drivers.csv"
drivers_data = pd.read_csv(drivers_file)

# Merge data with driver information
new_data = pd.merge(
    data, 
    drivers_data[['driver_number', 'name_acronym']],  
    on='driver_number', 
    how='left'
)

# Create the 'driver' column with name acronyms
new_data['driver'] = new_data['name_acronym']
new_data.drop(columns=['name_acronym'], inplace=True)

# Sidebar filters
st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", value=new_data['date'].min())
end_date = st.sidebar.date_input("End Date", value=new_data['date'].max())
category_filter = st.sidebar.multiselect("Category", options=new_data["category"].unique(), default=new_data["category"].unique())
flag_filter = st.sidebar.multiselect("Flag", options=new_data["flag"].dropna().unique(), default=new_data["flag"].unique())
scope_filter = st.sidebar.multiselect("Scope", options=new_data["scope"].dropna().unique(), default=new_data["scope"].unique())

# Apply filters when button is pressed
if st.sidebar.button("Apply Filters"):
    filtered_data = new_data[
        (new_data['date'] >= pd.Timestamp(start_date)) & 
        (new_data['date'] <= pd.Timestamp(end_date)) & 
        (new_data['category'].isin(category_filter) if category_filter else True) &
        (new_data['flag'].isin(flag_filter) if flag_filter else True) & 
        (new_data['scope'].isin(scope_filter) if scope_filter else True)
    ]
    
    # Remove driver_number column
    data_wo_dn = filtered_data.drop(columns=['driver_number'])

    # Update the 'driver' column with clickable links for drivers
    for idx, row in data_wo_dn.iterrows():
        if pd.notna(row['driver']):
            driver_link = f"[{row['driver']}](/?driver={row['driver']})"  # Create a clickable link
        else:
            driver_link = "None"
        data_wo_dn.at[idx, 'driver'] = driver_link

    # Display the filtered data as an HTML table with clickable links
    st.write(data_wo_dn.to_html(escape=False, index=False), unsafe_allow_html=True)

# Driver Information Page (if driver is selected)
query_params = st.experimental_get_query_params()
selected_driver = query_params.get("driver", [None])[0]

# If a driver is selected, show driver details on a separate page
if selected_driver:
    driver_info = drivers_data[drivers_data['name_acronym'] == selected_driver]
    
    if not driver_info.empty:
        st.header(f"Driver Information: {selected_driver}")
        st.write(f"### Name: {driver_info['full_name'].iloc[0]}")
        st.write(f"### Driver Number: {driver_info['driver_number'].iloc[0]}") 
        st.write(f"### Team: {driver_info['team_name'].iloc[0]}")
        st.write(f"### Nation: {driver_info['country_code'].iloc[0]}")
    else:
        st.write("Driver not found.")
else:
    # Display the main page with the events table if no driver is selected
    st.header("Formula 1 Events")
    st.write("Click on a driver's name to view their details.")
