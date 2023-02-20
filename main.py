import requests

api_source = "https://environment.data.gov.uk/flood-monitoring/id/stations/1491TH/readings?since=2023-02-17T23:23:00Z"

content_response = requests.get(api_source)

response_status = content_response.status_code
response_json = content_response.json()

print(response_status)
print(response_json)