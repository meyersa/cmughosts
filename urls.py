"""
Implementation to get URLs from Google search to add to scraping 

May not end up going this route since it doesn't return back a lot of information, 
but this is also a rough implementation for scraping the actual sites 
"""

from pymongo import MongoClient
import logging
import os
import requests

logging.info(f'Initializing Mongo')
MONGO_DB = MongoClient(os.getenv("MONGO_URL"))["cmughosts"]
logging.info(f'Initialized Mongo')


def saveURLs(urls: list[str]) -> bool:
    """
    Save URLs to Mongo to be scraped

    Inputs: 
        urls: list[str] of urls to save 

    Returns: 
        bool: status of upload
    """
    if type(urls) != list:
        logging.exception(f'Input is not the correct type')
        return False

    logging.info(f'Saving {len(urls)} URLs to Mongo')

    status = True
    count = 0
    urlDB = MONGO_DB['urls']

    for url in urls:
        logging.debug(f'Processing URL {count} of {len(urls)}: {url}')
        count += 1

        if not urlDB.find_one({"url": url}):
            status &= bool(urlDB.insert_one({"url": url}))
            continue

        logging.debug(f'Already seen URL, skipping')

    logging.info(f'Finished')
    return status


def getURLs() -> list[str]:
    """
    Get URLs from Google

    Returns: 
        list[str]: URLs found
    """
    logging.info(f'Getting URLs')

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

    def genParams(startIndex):
        return {
            "start": startIndex,
            "language": "lang_en",
            "safe": "off",
            "cx": GOOGLE_CSE_ID,
            "key": GOOGLE_API_KEY,
            "filter": "1",
            "gl": "US",
            "cr": "countryUS",
            "hl": "en",
            "exactTerms": "mount pleasant michigan",
            "orTerms": "haunt ghost apparition spooky evil",
            "fileType": "html"
        }

    results = list() 
    startIndex = 1 

    while True: 
        res = requests.get(GOOGLE_API_URL, params=genParams(startIndex))
        res = res.json()

        for item in res.get("items"): 
            results.append(item.get("link"))

        nextPage = res.get("queries").get("nextPage")
        if not nextPage: 
            break

        startIndex = nextPage[0].get("startIndex")

    return results

if __name__ == "__main__":
    saveURLs(getURLs())
