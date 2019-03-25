# pylint:disable=protected-access
# pylint:disable=unused-argument
import httmock
import requests
import bs4
from urllib.parse import urlparse
from functools import wraps

from source.crawling import druglistextractor


content = """
<body>
    <div class="searchResBlock" id="searchResBlock_11">
    <div class="SoegeresText">
            Søgeresultater, 
            Præparater
            :
    </div>
    <a class="glob-search_link" href="http://pro.medicin.dk/Medicin/Praeparater/1">
        AwesomeMed #1
    </a>
    <a class="glob-search_link" href="http://pro.medicin.dk/Medicin/Praeparater/2">
        AwesomeMed #2
    </a>
    <a class="glob-search_link" href="http://pro.medicin.dk/Medicin/Praeparater/3">
        AwesomeMed #3
    </a>
</body>
"""

soup = bs4.BeautifulSoup(content, 'html.parser')

VALIDSCHEME, VALIDNETLOC, VALIDPATH, _, VALIDQUERY, _ = urlparse(
    druglistextractor.baseurl + druglistextractor.searchurl + r'[a-z]'
)

validmockurl = 'http://validmockurl.com/'
VALIDMOCKSCHEME, VALIDMOCKNETLOC, VALIDMOCKPATH, _, VALIDMOCKQUERY, _ = urlparse(
    validmockurl + '' + r'[a-z]'
)

invalidmockurl = 'http://invalidmockurl.com/'
INVALIDMOCKSCHEME, INVALIDMOCKNETLOC, INVALIDMOCKPATH, _, INVALIDMOCKQUERY, _ = urlparse(
    invalidmockurl + '' + r'[a-z]'
)


@httmock.urlmatch(scheme=VALIDSCHEME, netloc=VALIDNETLOC, path=VALIDPATH, query=VALIDQUERY)
def search_url_mock_returns_valid_content(url: str, request: requests.Request):
    return {'status_code': 200, 'content': content}


@httmock.urlmatch(
    scheme=VALIDMOCKSCHEME, 
    netloc=VALIDMOCKNETLOC, 
    path=VALIDMOCKPATH, 
    query=VALIDMOCKQUERY
)
def search_url_valid_mock_returns_invalid_content(url: str, request: requests.Request):
    return {'status_code': 200, 'content': 'Invalid content'} 


@httmock.urlmatch(
    scheme=INVALIDMOCKSCHEME, 
    netloc=INVALIDMOCKNETLOC, 
    path=INVALIDMOCKPATH, 
    query=INVALIDMOCKQUERY
)
def search_url_invalid_mock_returns_invalid_content(url: str, request: requests.Request):
    return {'status_code': 400, 'content': 'Invalid content'} 


def usemockurl(mockurl: str):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            originalbaseurl = druglistextractor.baseurl
            originalsearchurl = druglistextractor.searchurl

            druglistextractor.baseurl = mockurl
            druglistextractor.searchurl = ''

            result = func(*args, **kwargs)

            druglistextractor.baseurl = originalbaseurl
            druglistextractor.searchurl = originalsearchurl
            return result
        return inner
    return decorator


def test_extractdruglistfrombs4_valid_soup(caplog):
    with httmock.HTTMock(search_url_mock_returns_valid_content):
        result = druglistextractor._extractdruglistfrombs4(soup)
        assert len(result) == 3
        assert not caplog.records


def test_extractdruglistfrombs4_invalid_soup(caplog):
    with httmock.HTTMock(search_url_mock_returns_valid_content):
        result = druglistextractor._extractdruglistfrombs4(
            bs4.BeautifulSoup('no content', 'html.parser')
        )
        assert result is None
        assert len(caplog.records) == 1
        assert 'Something went wrong parsing the soup.' in caplog.text


def test_extractdruglinksbyletter_letter_a_valid_crawl_valid_soup(caplog):
    with httmock.HTTMock(search_url_mock_returns_valid_content):
        result = druglistextractor._extractdruglinksbyletter('a')

        assert len(result) == 3
        assert not caplog.records


@usemockurl(validmockurl)
def test_extractdruglinksbyletter_letter_a_valid_crawl_invalid_soup(caplog):
    with httmock.HTTMock(search_url_valid_mock_returns_invalid_content):
        result = druglistextractor._extractdruglinksbyletter('a')

        assert result is None
        assert len(caplog.records) == 1
        assert 'Something went wrong parsing the soup.' in caplog.text


@usemockurl(invalidmockurl)
def test_extractdruglinksbyletter_letter_a_invalid_crawl(caplog):
    with httmock.HTTMock(search_url_invalid_mock_returns_invalid_content):
        result = druglistextractor._extractdruglinksbyletter('a')

        assert result is None
        assert len(caplog.records) == 1
        assert 'An error occured while crawling the letter' in caplog.text


def test_getdruglinklist_valid(caplog):
    oldpoliteness = druglistextractor.crawler.CONFIG['POLITENESS']
    druglistextractor.crawler.CONFIG['POLITENESS'] = 0
    with httmock.HTTMock(search_url_mock_returns_valid_content):
        result = druglistextractor.getdruglinklist()

        assert len(result) == 26

        total = sum([len(number) for _, number in result.items()])
        assert total == 26*3

        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == 'INFO'
        assert '(0 failed)' in caplog.text
    
    druglistextractor.crawler.CONFIG['POLITENESS'] = oldpoliteness


@usemockurl(validmockurl)
def test_getdruglinklist_invalid_contents(caplog):
    oldpoliteness = druglistextractor.crawler.CONFIG['POLITENESS']
    druglistextractor.crawler.CONFIG['POLITENESS'] = 0
    with httmock.HTTMock(search_url_valid_mock_returns_invalid_content):
        result = druglistextractor.getdruglinklist()

        assert len(result) == 26

        total = sum([len(number) for _, number in result.items() if number is not None])
        assert total == 0

        assert len(caplog.records) == 27
        assert caplog.records[-1].levelname == 'WARNING'
        for log in caplog.records[:-2]:
            assert log.levelname == 'ERROR'
        assert '(26 failed)' in caplog.text
    
    druglistextractor.crawler.CONFIG['POLITENESS'] = oldpoliteness