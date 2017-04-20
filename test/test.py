from datetime import datetime

if __name__ == '__main__':
    date1 = datetime.strptime("2016-09-01", "%Y-%m-%d")
    date2 = datetime.strptime("2016-09-02", "%Y-%m-%d")
    print (date1-date2).days
