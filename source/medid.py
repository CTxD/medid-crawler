import time
import logging

from .common import inttimestamp
from .config import CONFIG
from .crawler import crawler

logger = logging.getLogger(__name__)


def start(starttime: int = 0):
    crawlloop(starttime, 0)


def crawlloop(starttime: int = 0, iterations: int = 0):
    """
    Starts the crawling loop.
    - **parameters** ::
        - starttime:
            inttimestamp for when the crawling should begin.
            If starttime < time.time() the parameter is ignored.
            If not specified crawling will begin immediately
        - iterations:
            How many crawling iterations should be run
            If iterations <= 0 the parameter is ignored
            If not specified crawling will run indefinitively
    """
    now = inttimestamp.intnowstamp()

    if starttime > 0 and starttime >= now:
        delta = starttime-now
        logger.info(f'Starting next iteration in {delta} seconds')
        time.sleep(starttime-now)

    iterationcount = 0
    while(True):
        start = inttimestamp.intnowstamp()
        # Only increment the iterationcount if we have specified a max number of iterations
        if iterations:
            iterationcount += 1
        
        # ### INVOCATION OF CRAWLER ETC GOES HERE! ### #

        # If a max number of iterations has been specified and we have reached that limit, break
        if iterations and iterationcount == iterations:
            break
        
        # Sleep until next iteration
        end = inttimestamp.intnowstamp()
        if end-start < CONFIG['INTERVAL']:
            delta = CONFIG['INTERVAL'] - (end - start)
            logger.info(f'Starting next iteration in {delta} seconds')
            time.sleep(delta)
        
    logger.info('Crawling finished.')