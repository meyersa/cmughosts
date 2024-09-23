from pymongo import MongoClient
from bs4 import BeautifulSoup
import logging 
import os 
import requests 

logging.info(f'Initializing Mongo')
MONGO_DB = MongoClient(os.getenv("MONGO_URL"))["cmughosts"]
logging.info(f'Initialized Mongo')

def getURLs() -> list[str]: 
    """
    Get URLs from Mongo 
    
    Returns: 
        list[str]: of URLs
    """
    return [x.get("url") for x in MONGO_DB["urls"].find({}, {"_id": 0, "url": 1})]

def scrapeURL(url: str) -> None: 
    """
    Scrape URL for information from site
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    print(soup.get_text().strip()) 
    print() 

test = getURLs() 

for url in test: 
    scrapeURL(url) 

print(test)
