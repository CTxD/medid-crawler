import requests

from ..config import CONFIG


def crawl(url: str) -> None: # BS4 
    response = requests.get(url)
