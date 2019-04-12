"""
Wrapper for starting a crawling iteration.
"""
import logging
import source.common.firestore as fs
from . import druglistextractor
from . import druginfopageextracter


logger = logging.getLogger(__name__)


# REMOVE PRAGMA: NO COVER WHEN FUNCTION RECEIVES ACTUAL IMPLEMENTATION!
def start(): # pragma: no cover
    # 1. Get the list of drugs
    druglistdict = druglistextractor.getdruglinklist()
    pilldatabase = fs.FBManager()
    # 2. Give the list of drugs to the druginfoextractor and
    # 3. Feed the database with drugs from (above)
    logger.info('Getting drug info')
    successesbyletter = {}

    for letter, druglinklist in druglistdict.items():
        successesbyletter[letter] = 0
        if druglinklist is None:
            continue

        for druginfo in druginfopageextracter.getdata(druglinklist[:10]):
            logger.info('Finished getting pilldata for ' + druginfo.pillname) # noqa
            pilldatabase.add_or_update("pills", druginfo)
            successesbyletter[letter] += 1

    pilldatabase.update_crawling_meta(
        {
            'links_by_letter': {
                letter: len(links) if isinstance(links, list) else 'Null' 
                for letter, links in druglistdict.items()
            },
            'drugs_by_letter': successesbyletter
        }
    )