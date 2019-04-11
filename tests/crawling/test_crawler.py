# pylint:disable=protected-access
# pylint:disable=unused-argument
import pytest
import requests
import bs4
import httmock

from source.crawling import crawler
from source.common import inttimestamp
from source.config import CONFIG, readconfig

from urllib.parse import urlparse

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
        with httmock.HTTMock(urlmock_status_raises_requestexception):
            crawler.crawl('someinvalid.url')


def test_crawl_available_url_invalid_status_code():
    # Force non-compliance with politeness on our mockurls for faster test execution
    crawler._domainlastvisit['mockurl.com'] = 0

    with pytest.raises(requests.HTTPError):
        with httmock.HTTMock(urlmock_status_code_400):
            crawler.crawl('http://mockurl.com')


def test_crawl_available_url():
    # Force non-compliance with politeness on our mockurls for faster test execution
    crawler._domainlastvisit['mockurl.com'] = 0

    source = bs4.BeautifulSoup('Hello World!'.encode('utf-8'), 'html.parser')
    with httmock.HTTMock(urlmock_status_code_200):
        response = crawler.crawl('http://mockurl.com')
        assert response == source


def test_crawl_available_url_comply_politeness_1():
    now = inttimestamp.intnowstamp()
    
    # Force compliance with politeness on our mockurl to let it wait for 1 second in order to test
    # politeness compliance. 
    crawler._domainlastvisit['mockurl.com'] = now - CONFIG['POLITENESS'] + 1

    source = bs4.BeautifulSoup('Hello World!'.encode('utf-8'), 'html.parser')
    with httmock.HTTMock(urlmock_status_code_200):
        response = crawler.crawl('http://mockurl.com')
        assert response == source

        assert inttimestamp.intnowstamp() == pytest.approx(now + 1, 0.1)


VALIDSCHEME, VALIDNETLOC, VALIDPATH, _, VALIDQUERY, _ = urlparse('http://pro.medicin.dk/mockimagepath')
@httmock.urlmatch(scheme=VALIDSCHEME, netloc=VALIDNETLOC, path=VALIDPATH, query=VALIDQUERY)
def valid_image_url(url: str, request: requests.Request):
    return {'status_code': 200, 'content': 'something'}


def test_image_encoding():
    with httmock.HTTMock(valid_image_url):
        encoding_result = crawler.get_image_byte64_encoding("/mockimagepath")
    assert encoding_result == b'c29tZXRoaW5n'


INVALIDSCHEME, INVALIDNETLOC, INVALIDPATH, _, INVALIDQUERY, _ = urlparse('http://pro.medicin.dk/mockimagepathinvalid')
@httmock.urlmatch(scheme=INVALIDSCHEME, netloc=INVALIDNETLOC, path=INVALIDPATH, query=INVALIDQUERY)
def invalid_image_url(url: str, request: requests.Request):
    return {'status_code': 404, 'content': 'Not an image'}


def test_image_encoding_failing():
    with httmock.HTTMock(invalid_image_url):
        encoding_result = crawler.get_image_byte64_encoding("/mockimagepathinvalid")
    assert encoding_result is None


@httmock.urlmatch(netloc=r'(.*\.)?mockurl\.com$')
def urlmock_status_code_200(url: str, request: requests.Request): 
    return {'status_code': 200, 'content': 'Hello World!'}


@httmock.urlmatch(netloc=r'(.*\.)?mockurl\.com$')
def urlmock_status_code_400(url: str, request: requests.Request):
    return {'status_code': 400, 'content': 'Bad request!'}


def urlmock_status_raises_requestexception(url: str, request: requests.Request):
    pass
