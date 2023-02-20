import sys
import requests
from datetime import datetime, timedelta, timezone

import numpy as np # For easy sorting of dates
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Global constants --------------------------------------------------------------------------

api_source = 'https://environment.data.gov.uk/flood-monitoring/id/stations'
api_date_format = '%Y-%m-%dT%H:%M:%S%z'
api_date_format_nozulu = '%Y-%m-%dT%H:%M:%S'
display_date_format = "%b-%d %H:%M"
date_form = mdates.DateFormatter(display_date_format) # For matplotlib



# Functions ---------------------------------------------------------------------------------

def get_station_query_source(query_type):

    q = '?_limit=100'

    if query_type == 'LABEL':
        q = input('Type label or portion of label:\t')
        q = '?label='+q
    elif query_type == 'RIVER':
        q = input('Type exact river name:\t')
        q = '?riverName='+q
    elif query_type == 'RLOIid':
        q = input('Type exact RLOIid:\t')
        q = '?RLOIid='+q
    else:
        print('Invalid query type. Printing partial station list.\n')
    
    return api_source + q

def list_stations(stations_response):
    stations = stations_response.json()['items']
    found_stations = True
    
    if len(stations) != 0:
        print('--------------------------------')
        print('Station name:','stationReference')
        for station in stations:
            print('\"'+station['label']+'\":',station['stationReference'])
        print('--------------------------------\n')
    else:
        print('No stations found.')
        found_stations = False
    
    return found_stations


def run_station_finder_help():


    if len(sys.argv)==1: # Allow for user to input station code directly
        
        
        print('\nStation finder help -------------------------')
        print('Stations can be queried by LABEL, by RIVER, by RLOIid')
        query_type = input('Select query type:\t')
        
        query_source = get_station_query_source(query_type)
        stations_response = requests.get(query_source)

        found_stations = list_stations(stations_response)
        
        if not found_stations:
            query_source = get_station_query_source('na') # Redoes invalid query to get stations list
            stations_response = requests.get(query_source)
            list_stations(stations_response)

        station = input('Input station reference:\t')

    else:
        print('Taking first command line argument as station reference')
        station = sys.argv[1]

    if not station:
        station = 'na' # Prevents JSON errors when querying from API
        
    return station
    
def make_query_source(station):
    
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(hours=24)

    start_date = yesterday.strftime(api_date_format_nozulu)+'Z' # Adding Z automatically was tricky. Knowing the syntax for the API this is more reliable
    readings_request = "/readings?since="+start_date

    full_source = api_source+'/'+station+readings_request
    
    return full_source

def get_data(full_source):

    content_response = requests.get(full_source)

    response_status = content_response.status_code
    response_json = content_response.json()


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
    
    return all_measurements,dates


def sort_values(all_measurements,dates):
    
    for key in all_measurements.keys():
        sort_args = np.argsort(dates[key]) # Gets correct order of the elements
        dates[key] = np.array(dates[key])[sort_args] # Orders the dates
        all_measurements[key] = np.array(all_measurements[key])[sort_args]
    
    return all_measurements,dates


def check_graph_count(keys):

    if len(keys) == 0:
        print('Station not found or data not available')
        quit()
    else:
        print('Creating {} graph(s):'.format(len(keys)))
        for key in keys:
            print('\t {}'.format(key))
    
    return None

def generate_plot(x,y,station):
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
    
    return None



# Execution ----------------------------------------------------------------------------------------------------------

station = run_station_finder_help()

full_source = make_query_source(station)

all_measurements,dates = get_data(full_source)

sort_values(all_measurements,dates)

keys = all_measurements.keys()

check_graph_count(keys)


for key in keys:
    
    x = dates[key]
    y = all_measurements[key]
    
    generate_plot(x,y,station)
    
