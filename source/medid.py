import time
import logging

from .common import inttimestamp
from .config import CONFIG


logger = logging.getLogger(__name__)


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
    delta = starttime - inttimestamp.intnowstamp()
    
    # Only wait if the starttime supplied is a future timestamp
    if starttime and delta > 0:
        logger.info(f'Starting next iteration in {delta} seconds')
        time.sleep(delta)

    # If a negative number of iterations has been specified we set it to 0 in order to ignore it
    if iterations < 0: # pragma: no cover
        iterations = 0

    iterationcount = 0

    # While-true's with inbuilt conditional breaks are seldom the right way to handle looping
    # but doing it this way gives us two benefits:
    #   1. Iterationscount is only incremented if a max number of iterations has been specified. 
    #       We do, in other words, not have to keep track of a control variable if not needed.
    #   2. We conditionally break out of the loop if a max number of iterations has been specified 
    #       and reached. We do this *before* the thread sleeps until next iteration - which, by 
    #       is a period of 14 days. 
    while(True):
        if iterations:
            iterationcount += 1

        # ########## CRAWLING PROCESS BEGIN ########### #
        start = inttimestamp.intnowstamp()

        # NOTE! When implemented the tests for medid has to be adjusted to remove the reference to
        # the crawler.process (or whatever name it gets), so that it doesn't run as part of the 
        # tests for medid. E.g. we test crawlloop without actually crawling anything!        
        # start crawler.process here #

        end = inttimestamp.intnowstamp()
        # ########### CRAWLING PROCESS END ############ #
    
        logger.info(f'Iteration finished in {end - start} seconds.')
       
        # If a number of iterations has been specified and reached, break the loop
        # We break out of the loop this way in order to not wait for time.sleep to finish before
        # breaking out of the loop.
        if iterations and iterationcount == iterations:
            break

        # Sleep until next iteration
        if end-start < CONFIG['INTERVAL']:
            delta = CONFIG['INTERVAL'] - (end - start)
            logger.info(f'Starting next iteration in {delta} seconds.')
            time.sleep(delta)
        
    logger.info('Crawling finished.')