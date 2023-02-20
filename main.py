import requests

api_source = "https://environment.data.gov.uk/flood-monitoring/id/stations/"
station = "1491TH"
date = "2023-02-17T23:23:00Z"
readings_request = "/readings?since="+date

full_source = api_source+station+readings_request

content_response = requests.get(full_source)

response_status = content_response.status_code
response_json = content_response.json()

print(response_status)

all_measurements = {}

for item in response_json['items']:
    measure = item['measure'].split('/')[-1]
    value = item['value']
    if measure not in all_measurements.keys():
        all_measurements[measure] = [value] 
        print('New measure '+measure+' '+str(value))
    else:
        print(value)
    