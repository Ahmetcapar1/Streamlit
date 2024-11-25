import requests
import pandas

url="https://api.openf1.org/v1/race_control"
response = requests.get(url)
response_json = response.json()
data = pandas.DataFrame(response_json)
datafilter = data[data['category'] != 'Other']
columns_to_drop = ['session_key', 'meeting_key', 'sector']
filtered_data = datafilter.drop(columns=columns_to_drop)
filtered_data['date'] = filtered_data['date'].str[:10]
filtered_data.to_csv("data.csv",index= False)  
grouped_data = filtered_data.groupby('date')

print(grouped_data.size())  