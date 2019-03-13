"""Get the current Unix Epoch timestamp as an integer"""
import time


def intnowstamp() -> int:
    """Get the current Unix Epoch timestamp as an integer"""
    return int(time.time())