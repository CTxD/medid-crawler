"""
General crawling functionality.
"""

import time
import base64

from typing import Dict
from urllib.parse import urlsplit

import requests
import bs4

from ..common import inttimestamp
from ..config import CONFIG

# Dict of domains as keys and int timestamps of when they were last crawled.
# Don't do manual lookups in the dict to find out whether a domain can be crawled again!
# Use the _complypoliteness function, as this also makes sure to prune domains which can be visited!
_domainlastvisit: Dict[str, int] = {}


def _complypoliteness(url: str) -> int:
    """
    Takes as input a url and returns how many seconds (round up) until the url can be crawled again.
    """
    domain = getdomain(url)

    # If the domain has not yet been crawled, we can crawl it immediately
    if domain not in _domainlastvisit:
        return 0

    # Get the time (in seconds) until we can crawl the domain again
    delta = CONFIG['POLITENESS'] - \
        (inttimestamp.intnowstamp() - _domainlastvisit[domain])

    # If the time since our last crawl of this domain exceeds our POLITENESS factor, we prune the
    # domain from the dict and return 0, indicating we can crawl the domain immediately
    if delta <= 0:
        del _domainlastvisit[domain]
        return 0

    # Else, we return the number of seconds until we can crawl the domain again
    return delta


def getdomain(url: str) -> str:
    """
    Get the domain part of a url.

    Examples:
    http://www.google.com => google.com
    google.com:8080 => google.com
    google.com/search => google.com
    """
    splitresult = urlsplit(url.lower())

    # E.g. http://www.google.com/ => google.com
    domain = splitresult.netloc if splitresult.scheme.startswith(
        'http') else splitresult.scheme

    # For non-http urls, the entire url is considered a path
    # E.g. www.google.com/something => google.com
    if not domain:
        domain = splitresult.path.split('/')[0]

    # Remove any port information
    # E.g. google.com:8080 => google.com
    domain = domain.split(':')[0]

    # Remove www.
    # E.g. www.google.com => google.com
    if 'www.' in domain:
        domain = domain.split('www.')[1]

    return domain


def crawl(url: str) -> bs4.BeautifulSoup:
    """
    Crawls a url and returns a BeautifulSoup object of the response.

    The caller is responsible for handling exceptions!
    """
    if not url.startswith('http'):
        url = 'http://' + url
    # Check if the url domain can be crawled again
    # If _complypoliteness returns > 0, time.sleep() that amount of time
    delta = _complypoliteness(url)
    if delta > 0:
        time.sleep(delta)

    # Add entry in _domainlastvisit for inttimestamp (now in int)
    _domainlastvisit[getdomain(url)] = inttimestamp.intnowstamp()
    try:
        # Crawl page
        response = requests.get(url, timeout=CONFIG['TIMEOUT'])

    # All errors raised by requests inherit from RequestException
    except requests.RequestException as e:
        raise e

    # Check to see the response status code
    # Anything not in [200;299] raises an error
    if response.status_code < 200 or response.status_code > 299:
        raise requests.HTTPError(response=response)

    # If status code is 2xx, parse the response to a BeautifulSoup instance and return it
    source = bs4.BeautifulSoup(response.text.encode('utf-8'), 'html.parser')

    return source


def get_image_byte64_encoding(relative_url: str):
    # IMPORTANT!
    # URL that we receive misses http://pro.medicin.dk

    # TO DECODE:
    # imgdata = base64.b64decode(imgstring)
    # filename = 'some_image.jpg'
    # with open(filename, 'wb') as f:
    #     f.write(imgdata)

    img_url = "http://pro.medicin.dk" + relative_url

    delta = _complypoliteness(img_url)
    if delta > 0:  # pragma: no cover
        time.sleep(delta)

    return base64.b64encode(requests.get(img_url).content)
