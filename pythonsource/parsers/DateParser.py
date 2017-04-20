from datetime import datetime


def StraitsTimesDateParse(datestring):
    try:
        d = datetime.strptime(datestring.decode('utf-8'), '%Y:%m:%d %H:%M:%S').date()
    except:
        print "error"
        return datetime.date("1970-01-01")
    return d


def TodayOnlineDateParse(datestring):
    try:
        d = datetime.strptime(datestring, '%Y%m%d').date()
    except:
        return datetime.date("1970-01-01")
    return d


def ChannelAsiaDateParse(datestring):
    try:

        datestring = datestring.replace('Posted', '').strip()
        d = datetime.strptime(datestring, '%d %b %Y %H:%M').date()
    except:
        print "error"
        return datetime.date("1970-01-01")
    return d


def MotherShipDateParse(datestring):
    try:

        d = datetime.strptime(datestring, '%B %d, %Y').date()
    except:
        print "error"
        return datetime.date("1970-01-01")
    return d


def AllSingaporeStuffDateParse(datestring):
    try:
        d = datetime.strptime(datestring[:len(datestring) - 6], '%Y-%m-%dT%H:%M:%S').date()
    except:
        print "error"
        return datetime.date("1970-01-01")
    return d


def MustShareNewsDateParse(datestring):
    try:
        d = datetime.strptime(datestring[:len(datestring) - 6], '%Y-%m-%dT%H:%M:%S').date()
    except:
        print "error"
        return datetime.date("1970-01-01")
    return d
