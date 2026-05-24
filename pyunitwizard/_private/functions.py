import sys

def caller_name(skip=3):
    try:
        return sys._getframe(skip).f_code.co_name
    except ValueError:
        return "unknown"

