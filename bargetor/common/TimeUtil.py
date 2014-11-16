import datetime

def str_to_date(str, format = "%Y-%m-%d %H:%M:%S"):
    if not str:
        return None
    if isinstance(str, datetime.datetime):
        return str
    return datetime.datetime.strptime(str, format)

# print type(str_to_date('2014-09-12 12:12:12'))
