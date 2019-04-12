import re
import logging
from typing import Dict, List, Union
from string import ascii_lowercase

from bs4 import BeautifulSoup

from . import crawler

logger = logging.getLogger(__name__)

baseurl = 'http://pro.medicin.dk'
searchurl = '/Search/Search/SearchAlpha/'


def getdruglinklist() -> Dict[str, Union[List[str], None]]:
    letterdict: Dict[str, Union[List[str], None]] = {}
    
    # Iterate letters from a-z
    for letter in ascii_lowercase:
        links = _extractdruglinksbyletter(letter)
        # If a list of links is returned, we cast it to set and back to list in order to remove any
        # duplicate links.
        letterdict[letter] = list(set(links)) if isinstance(links, list) else links
        logger.info(
            f'Links for letter {letter}: {len(letterdict[letter]) if letterdict[letter] else "None"}' # type: ignore # noqa
        )
        
    # Prepare a log message according to the results getting the drug link list
    loghandler = logger.info
    total = 0
    failed = 0
    letterinfo = ''
    for letter, result in letterdict.items():
        if result is None:
            loghandler = logger.warning
            failed += 1
        else:
            total += len(result)
        
        letterinfo += f'{letter}: {len(result) if isinstance(result, list) else "None"}; '
    
    letterinfo = letterinfo[:-2]
    loghandler( # noqa
        f'Drug link list extracted: {total} links extracted from {len(letterdict)-failed} letters '
        f'({failed} failed): ' + letterinfo
    )

    return letterdict


def _extractdruglinksbyletter(letter: str) -> Union[List[str], None]:
    url = baseurl + searchurl + letter.lower()

    try:
        soup = crawler.crawl(url)

    # crawler.crawl re-raises all exceptions, so we have to catch and handle them accordingly here.
    except Exception as e:
        logger.error(
            f'An error occured while crawling the letter "{letter}". The following exception was '
            f'raised: {type(e)} :: {str(e)}'
        )
        return None

    return _extractdruglistfrombs4(soup)


def _extractdruglistfrombs4(soup: BeautifulSoup) -> Union[List[str], None]:
    try:
        drugslistraw = soup.find(
            'div', 
            attrs={'class': 'SoegeresText'}, 
            string=re.compile('Præparater')
        ).parent.find_all(
            'a', 
            'glob-search_link'
        )
   
        return [baseurl + link.get('href') for link in drugslistraw]
    
    # Exceptions raised here are because the format of the soup does not correspond with the 
    # expected format, from which we try to extract drug links. 
    except Exception as e:
        logger.error(
            'Something went wrong parsing the soup. Perhaps the format of the soup is invalid. '
            f'The following exceptions was raised: {type(e)} :: {str(e)}'
        )
        return None
