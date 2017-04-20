import mysql.connector
from mysql.connector import Error
from utils.Config import BackColors, DbConfig
from utils.Paths import Paths


def ParseKeywords(year, month):
    global cursor, cnn
    f = open(Paths.keywordspath + str(year) + str(month) + '.txt', 'w')
    try:
        cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        cursor = cnn.cursor(buffered=True)
        sqlquery = 'Select keyword from straitstimesdata where postyear = ' + str(year) + ' And postmonth = ' + str(
            month)
        cursor.execute(sqlquery)
        row = cursor.fetchone()
        while row is not None:
            f.write(row[0] + '\n')
            row = cursor.fetchone()
        f.close()
    except Error as e:
        print BackColors.WARNING + "error" + BackColors.ENDC
        print e
    finally:
        cursor.close()
        cnn.close()
