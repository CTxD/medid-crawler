"""
Wrapper for starting a crawling iteration.
"""

from . import druglistextractor


# REMOVE PRAGMA: NO COVER WHEN FUNCTION RECEIVES ACTUAL IMPLEMENTATION!
def start(): # pragma: no cover
    druglistextractor.getdruglinklist()
