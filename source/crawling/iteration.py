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
    for _, druglinklist in druglistdict.items():
        if druglinklist is None:
            continue
        
        for druginfo in druginfopageextracter.getdata(druglinklist[0:3]):
            logger.info('Finished getting pilldata for ' + druginfo.pillname) # noqa
            pilldatabase.add_or_update("pills", druginfo)
        break
