import requests
import pandas

url="https://api.openf1.org/v1/drivers"
response = requests.get(url)
response_json = response.json()
data = pandas.DataFrame(response_json)
columns_dropped = ['broadcast_name', 'team_colour','first_name','last_name','headshot_url', 'session_key', 'meeting_key']
filtered_data = data.drop(columns=columns_dropped)
final_data = filtered_data.head(17)
final_data.to_csv("F1_Drivers.csv", index=False)
print(final_data.to_string(index=False))