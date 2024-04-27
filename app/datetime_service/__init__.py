"""_summary_

Returns:
    _type_: _description_
"""

from datetime import datetime, timedelta


def getDateTimeLimit(next_day: int):
    """_summary_
    Args:
        next_day (int): _description_
    Returns:
        _type_: _description_
    """
    return datetime.now() + timedelta(days=next_day)
