import requests
from lxml.html import fromstring

params = {
    "query": "variety:sent",
    "request_date_after": "2024/09/01",
    "request_date_before": "2024/09/30",
}

response = requests.get("https://www.asktheeu.org/en/list/all", params=params)

print(response.text)
