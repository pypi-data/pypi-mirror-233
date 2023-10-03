import pandas as pd
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import json

def day_plus_one(day):
    return (datetime.strptime(day, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

def day_string_to_dt(day):
    return datetime.strptime(day, '%Y-%m-%d')

def get_incidents(user_name, password, url, endpoint, current_day, end_day, start_hour=0, hour_interval=8):
    all_records = []

    while day_string_to_dt(current_day) <= day_string_to_dt(end_day):
        start_hour = 0

        while start_hour < 24:
            print(f"Starting Interval: {len(all_records)}")

            query_string = f"opened_atBETWEENjavascript:gs.dateGenerate('{current_day}','{start_hour}:00:00')@javascript:gs.dateGenerate('{current_day}','{start_hour+hour_interval-1}:59:59')"
            payload = {'start': 0, 'count': 2000, 'encoded_query': query_string}
            json_data = requests.post(url + endpoint, data=json.dumps(payload), auth=HTTPBasicAuth(user_name, password)).json()

            records = pd.DataFrame(json_data['result']['records'])
            all_records.append(records)

            print(f"  Count of interval {len(all_records) - 1}: {len(records)}")

            start_hour += hour_interval

        current_day = day_plus_one(current_day)

    return pd.concat(all_records, axis=0, ignore_index=True)

