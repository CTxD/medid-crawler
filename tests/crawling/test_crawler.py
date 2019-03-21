# pylint:disable=protected-access
import pytest
import requests
import bs4

from source.crawling import crawler
from source.common import inttimestamp
from source.config import CONFIG, readconfig


readconfig('config.cfg')


@pytest.mark.parametrize("test_input, expected", [
    ('http://google.com', "google.com"),
    ('http://google.com/something', "google.com"),
    ('http://google.com:8080/something', "google.com"),
    ('www.google.com', "google.com"),
    ('www.google.com/something', "google.com"),
    ('www.google.com:8080/something', "google.com"),
    ('http://wwww.google.com/', "google.com"),
    ('http://www.google.com/something?query=somequery', "google.com")
])
def test_getdomain_googledomains(test_input, expected):
    assert crawler.getdomain(test_input) == expected


def test_complypoliteness_uncrawled_domain():
    assert crawler._complypoliteness("localhost.com") == 0 


def test_complypoliteness_crawled_domain_not_exceeding_politeness():
    domain = 'google.com'
    now = inttimestamp.intnowstamp()
    delta = 2 if CONFIG['POLITENESS'] > 3 else 1
    previous = now - delta

    # Insert entry in the domainlastvisit dict with our test setups
    crawler._domainlastvisit[domain] = previous 

    # _complypoliteness should return a value between 0 and POLITENESS value AND the domain should
    # remain in the _domainlastvisit dict
    assert crawler._complypoliteness(domain) == CONFIG['POLITENESS'] - delta 
    assert domain in crawler._domainlastvisit
    

def test_complypoliteness_crawled_domain_exceeding_politeness():
    domain = 'google.com'
    now = inttimestamp.intnowstamp()
    # Pretend we crawled a url 10 times the POLITENESS value ago. I.e. we very much exceed the 
    # POLITENESS value!
    previous = now - CONFIG['POLITENESS']*10

    # Insert entry in the domainlastvisit dict with our test setups
    crawler._domainlastvisit[domain] = previous 

    # _complypoliteness should return 0 AND the domain sohuld be removed from the _domainlastvisit 
    # dict
    assert crawler._complypoliteness(domain) == 0 
    assert domain not in crawler._domainlastvisit 


def test_crawl_unavailable_url():
    with pytest.raises(requests.RequestException):
        crawler.crawl('someinvalidurl.dk')


def test_crawl_available_url_invalid_status_code():
    with pytest.raises(requests.HTTPError):
        crawler.crawl('https://httpstat.us/400')


def test_crawl_available_url():
    source = bs4.BeautifulSoup('200 OK'.encode('utf-8'), 'html.parser')
    assert crawler.crawl('https://httpstat.us/200') == source
    
    