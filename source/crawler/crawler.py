import requests
import bs4

# from ..config import CONFIG


def crawl(url: str) -> bs4.BeautifulSoup:
    response = requests.get(url)
    source = bs4.BeautifulSoup(response.text.encode('utf-8'), 'html.parser')

    return source