import warnings
import requests
import logging
from lxml.html import fromstring

warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger().setLevel(logging.INFO)


def get_publications_page(index=0):
    params = {
        "sort": "publication_date",
        "sortorder": "desc",
        "q": "",
        "doctype[]": [
            # "dossier",
            "dossier.publication",
            # "dossier.document",
            # "dossier.woo_decision_main_document",
            # "dossier.attachment",
        ],
        # "dt[from]": "2023-01-01",
        # "dt[to]": "2024-02-01",
        "page": index + 1,
        "size": 100,
    }

    response = requests.get("https://open.minvws.nl/zoeken", params=params)

    doc = fromstring(response.text)

    # Get links to publications
    anchors = doc.findall('.//a[@data-e2e-name="main-link"]')

    for anchor in anchors:
        path = anchor.get("href").replace("\\", "")
        yield f"https://open.minvws.nl{path}"

    # Get publication
    # response = requests.get(url)
    # doc = fromstring(response.text)

    # Loop through pages of linked documents


def store_publication(url: str):
    print(url)


index = 0

while True:
    publication_urls = list(get_publications_page(index))
    if len(publication_urls) == 0:
        break

    for url in publication_urls:
        store_publication(url)

    index += 1
