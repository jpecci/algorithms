import datetime as dt


def get_time(timestamp):
    """timestamp in the form of yyyymmddhhmmss"""
    return timestamp % 1000000


def get_date(timestamp):
    """timestamp in the form of yyyymmddhhmmss"""
    return timestamp // 1000000


def get_sec(timestamp):
    """timestamp in the form of hhmmss"""
    return timestamp % 100


def get_min(timestamp):
    """timestamp in the form of hhmmss"""
    return (timestamp // 100) % 100


def get_hour(timestamp):
    """timestamp in the form of hhmmss"""
    return timestamp // 10000


def get_day(timestamp):
    """timestamp in the form of yyyymmdd"""
    return timestamp % 100


def get_month(timestamp):
    """timestamp in the form of yyyymmdd"""
    return (timestamp // 100) % 100


def get_year(timestamp):
    """timestamp in the form of yyyymmdd"""
    return timestamp // 10000


def range_date(start, end, delta=dt.timedelta(days=1)):
    next = start
    while next < end:
        yield next
        next += delta


if __name__ == '__main__':
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime(2015, 1, 10)
    delta = dt.timedelta(days=2)
    it = range_date(start, end, delta)
