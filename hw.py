import requests
import pandas

url="https://api.openf1.org/v1/race_control"
response = requests.get(url)
response_json = response.json()
data = pandas.DataFrame(response_json)
datafilter = data[data['category'] != 'Other']
columns_to_drop = ['session_key', 'meeting_key', 'sector']
filtered_data = datafilter.drop(columns=columns_to_drop)
filtered_data.to_csv("check.csv",index= False)
flags = filtered_data[filtered_data['category'] == 'Flag']
flags.to_csv("flags.csv",index=False)
flags['date'] = flags['date'].str[:10]  
grouped_flags = flags.groupby('date')
for date_group, group_data in grouped_flags:
    group_data.to_csv(f"flags{date_group}.csv", index=False)
print(grouped_flags.size())  
flags.to_csv("flags.csv",index=False)