"""
Wrapper for starting a crawling iteration.
"""

from . import druginfopageextracter


def start():
    druginfopageextracter.main()
    