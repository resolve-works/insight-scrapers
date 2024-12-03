from os import environ as env
import requests
import logging
from os.path import splitext
from urllib.parse import urlparse
from lxml.html import fromstring
from lxml.etree import _Element

logging.basicConfig(level=logging.INFO)


def get_pdf_hrefs(doc: _Element):
    anchors = doc.findall('.//li[@class="attachment"]/a')
    # Filter PDF attachments
    for anchor in anchors:
        href = anchor.get("href")
        yield urlparse(href).path


def scrape_request(id: int):
    response = requests.get(f"https://www.asktheeu.org/en/request/{id}")

    doc = fromstring(response.text)
    name = doc.find('.//div[@class="request-header"]//h1').text

    pdf_hrefs = list(get_pdf_hrefs(doc))

    if len(pdf_hrefs) > 0:
        # Create insight folder

        # Upload PDFs


# for href in scrape_index():
# scrape_request(href)

scrape_request(15164)
