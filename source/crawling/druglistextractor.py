from typing import List
from string import ascii_lowercase

from bs4 import BeautifulSoup

from . import crawler


def getdruglinklist() -> List[str]:
    druglinklist: List[str] = []

    # Iterate from a-z
    for letter in ascii_lowercase:
        druglinklist.extend(_extractdruglinksbyletter(letter))

    return druglinklist


def _extractdruglistfrombs4(soup: BeautifulSoup) -> List[str]:
    return [soup.decode]


def _extractdruglinksbyletter(letter: str) -> List[str]:
    url = 'http://pro.medicin.dk/Search/Search/SearchAlpha/' + letter.lower()
    soup = crawler.crawl(url)
    return _extractdruglistfrombs4(soup)