import time

import pytest

from source import medid
from source.config import config
from source.crawling import iteration

config.readconfig('config.cfg')

# Set the number of seconds between iterations to 1 second for testing purposes
config.CONFIG['INTERVAL'] = 1

# Monkey-patch the crawling iteration to a lambda function which does nothing
iteration.start = lambda: None 


@pytest.mark.parametrize("test_input, expected", [
    (1, 0),
    (2, 1)
])
def test_crawlloop_various_iterations(test_input: int, expected: int):
    start = time.time()
    medid.crawlloop(0, test_input)
    delta = int(time.time() - start)

    assert delta == pytest.approx(expected)


def test_crawlloop_delayed_start():
    starttime = int(time.time())+2
    start = time.time()
    medid.crawlloop(starttime, 1)
    delta = int(time.time() - start)

    assert delta == pytest.approx(2)


