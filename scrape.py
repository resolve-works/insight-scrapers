from time import sleep
import requests
import logging
from os.path import splitext
from pathlib import Path
from io import BytesIO
from urllib.parse import urlparse, unquote
from lxml.html import fromstring
from lxml.etree import _Element
from insightclient import InsightClient

logging.getLogger().setLevel(logging.INFO)


def get_attachment_paths(doc: _Element):
    anchors = doc.findall('.//li[@class="attachment"]/a')
    # Filter PDF attachments as a lot of the attachments come from an email
    # system that also includes things like EU logos used in emails etc
    for anchor in anchors:
        href = anchor.get("href")
        path = urlparse(href).path
        _, extension = splitext(path)
        if extension == ".pdf":
            yield path


# Get latest request url
response = requests.get("https://www.asktheeu.org/en/list/all")
doc = fromstring(response.text)
anchor = doc.find(".//div[@class='request_left']//span[@class='head']/a")

# Get ID from latest published request
response = requests.get(f"https://www.asktheeu.org{anchor.get('href')}")
doc = fromstring(response.text)
anchor = doc.find(".//ul[@class='action-menu__menu__submenu owner_actions']/li/a")
url = urlparse(anchor.get("href"))
last_id = int(Path(url.path).name)

insight = InsightClient()

root_inode = insight.create_folder("AsktheEU", is_public=True)

id = 1
while id <= last_id:
    response = requests.get(f"https://www.asktheeu.org/en/request/{id}")
    if response.status_code != 200:
        id += 1
        continue

    doc = fromstring(response.text)
    name = doc.find('.//div[@class="request-header"]//h1').text
    folder_name = f"{id} - {name}"
    attachment_paths = list(get_attachment_paths(doc))
    logging.info(f"Processing {folder_name}")

    if len(attachment_paths) > 0:
        logging.info(f"Found {len(attachment_paths)} attachments")
        # Create insight folder
        parent = insight.create_folder(folder_name, root_inode["id"], is_public=True)

        # Upload PDFs
        for path in attachment_paths:
            try:
                with requests.get(
                    f"https://www.asktheeu.org{path}", stream=True
                ) as response:
                    response.raise_for_status()

                    name = unquote(Path(path).name)
                    num = Path(path).parent.name
                    attachment_name = f"{num} {name}"
                    logging.info(f"Storing {attachment_name}")

                    stream = BytesIO(response.content)
                    size = stream.getbuffer().nbytes
                    insight.create_file(
                        attachment_name, size, stream, parent["id"], is_public=True
                    )
                    sleep(1)
            except requests.exceptions.HTTPError as e:
                # Could be server does not respond
                logging.error(e)

    sleep(1)
    id += 1
