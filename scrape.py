import requests
from datetime import datetime, timedelta
from lxml.html import fromstring


# AskTheEU for some reason limits their pages to max 20. To fetch all requests
# we fetch per month to not exceed this arbitrary limit
def scrape_index(after: datetime, before: datetime):
    params = {
        "query": "variety:sent",
        "request_date_after": after.strftime("%Y/%m/%d"),
        "request_date_before": before.strftime("%Y/%m/%d"),
        "page": 1,
    }

    response = requests.get("https://www.asktheeu.org/en/list/all", params=params)

    doc = fromstring(response.text)

    for element in doc.findall(
        './/div[@class="request_listing"]//span[@class="head"]/a'
    ):
        yield element.get("href")


after = datetime.now().replace(day=1)
before = after.replace(month=after.month + 1)

print(list(scrape_index(after, before)))
