import requests
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from lxml.html import fromstring

logging.basicConfig(level=logging.INFO)


# AskTheEU for some reason limits their pages to max 20. To fetch all requests
# we limit to a date range to not exceed this arbitrary limit
def scrape_index_date_range(after: datetime, before: datetime):
    params = {
        "query": "variety:sent",
        "request_date_after": after.strftime("%Y/%m/%d"),
        "request_date_before": before.strftime("%Y/%m/%d"),
        "page": 1,
    }

    while True:
        logging.info(
            f"Scraping index {params['request_date_after']} to {params['request_date_before']} page {params['page']}"
        )
        response = requests.get("https://www.asktheeu.org/en/list/all", params=params)

        doc = fromstring(response.text)

        elements = doc.findall(
            './/div[@class="request_listing"]//span[@class="head"]/a'
        )

        if len(elements) < 1:
            break

        for element in elements:
            yield element.get("href")

        params["page"] += 1


def scrape_index():
    after = datetime.now().replace(day=1)

    while True:
        if after.year < 2024:
            break

        before = after.replace(month=after.month + 1)
        for href in scrape_index_date_range(after, before):
            yield href

        after -= relativedelta(months=1)


hrefs = list(scrape_index())

print(hrefs)
