"""
Wrapper for starting a crawling iteration.
"""

from . import druglistextractor


def start():
    druglistextractor.getdruglinklist()
    