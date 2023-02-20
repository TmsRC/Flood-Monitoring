import sys
import requests
from datetime import datetime, timedelta, timezone

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

if len(sys.argv)==2:
    argument = sys.argv[1]
else:
    argument = input('Input station code:\t')

now = datetime.now(timezone.utc)
yesterday = now - timedelta(hours=24)

api_date_format = '%Y-%m-%dT%H:%M:%S%z'
api_date_format_nozulu = '%Y-%m-%dT%H:%M:%S'

api_source = "https://environment.data.gov.uk/flood-monitoring/id/stations/"
station = "1491TH"
start_date = yesterday.strftime(api_date_format_nozulu)+'Z' # Adding Z automatically was tricky. Knowing the syntax for the API this is more reliable
readings_request = "/readings?since="+start_date

station = argument
full_source = api_source+station+readings_request

content_response = requests.get(full_source)

response_status = content_response.status_code
response_json = content_response.json()

# print(response_status)

all_measurements = {}
dates = {}

for item in response_json['items']:
    measure = item['measure'].split('/')[-1]
    value = item['value']
    measurement_date = datetime.strptime(item['dateTime'],api_date_format)
    if measure not in all_measurements.keys():
        all_measurements[measure] = [value] 
        dates[measure] = [measurement_date]
    else:
        all_measurements[measure].append(value)
        dates[measure].append(measurement_date)
        
for key in all_measurements.keys():
    sort_args = np.argsort(dates[key]) # Gets correct order of the elements
    dates[key] = np.array(dates[key])[sort_args] # Orders the dates
    all_measurements[key] = np.array(all_measurements[key])[sort_args]
    
keys = all_measurements.keys()
display_date_format = "%b-%d %H:%M"
date_form = mdates.DateFormatter(display_date_format)

if len(keys) == 0:
    print('Station not found or data not available')
else:
    print('Creating {} graphs:'.format(len(keys)))
    for key in keys:
        print('\t {}'.format(key))

    
for key in keys:
    
    x = dates[key]
    y = all_measurements[key]
    text_dates = [date.strftime(display_date_format) for date in x]
    
    table_cols = text_dates[::4]
    table_values = all_measurements[key][::4]
    table_text = np.resize(table_values,(1,len(table_values)) )
    
    plt.figure(figsize=(20,5))
    
    fig = plt.subplot(211)
    plt.plot(x,y)
    plt.xticks(x[::4],rotation=60,ha='right')
    ylabel = ''.join(key.split('-')[1:])
    plt.ylabel(ylabel)
    plt.grid()
    fig.axes.get_xaxis().set_major_formatter(date_form)
    
    
    fig = plt.subplot(212)
    plt.table(cellText = table_text,rowLabels=['Measurement'],rowLoc='center',colLabels=table_cols,loc='center')
    plt.box(on=None)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    
    plt.suptitle('Station '+station)
    plt.show()