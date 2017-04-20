import mysql.connector
from mysql.connector import Error
from utils.Config import BackColors, DbConfig
from pandas import DataFrame
from utils.Paths import Paths
import re

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


def StraitsTimesToCsv():
    rowList = []
    try:
        cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        cursor = cnn.cursor(buffered=True)
        sqlquery = 'Select category,content from newsdata.straitstimesdata'
        cursor.execute(sqlquery)
        row = cursor.fetchone()
        while row is not None:
            rowList.append({'category': row[0], 'content': TextProcess(row[1])})
            row = cursor.fetchone()
    except Error as e:
        print BackColors.WARNING + "error" + BackColors.ENDC
        print e
    df = DataFrame(rowList)
    df.to_csv(Paths.csvpath + 'straitstimes.csv')


def TodayOnineToCsv():
    categoryList = ['Community ', 'Consumer ', 'Crime/Court ', 'Defaut', 'Defence/Security ', 'Economy ', 'Education ',
                    'Environment ', 'Foreign Affairs ', 'Healthcare ', 'Local Politics (General) ', 'Manpower ',
                    'Others ', 'Property ', 'Transport ']

    rowList = []
    try:
        cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        cursor = cnn.cursor(buffered=True)
        sqlquery = 'Select category,content from newsdata.todayonlinedata'
        cursor.execute(sqlquery)
        row = cursor.fetchone()
        i = 1
        while row is not None:
            if row[0] in categoryList:
                print i
                i += 1
                rowList.append({'category': row[0], 'content': TextProcess(row[1])})
            row = cursor.fetchone()
    except Error as e:
        print BackColors.WARNING + "error" + BackColors.ENDC
        print e
    print "2"
    df = DataFrame(rowList)
    df.to_csv(Paths.csvpath + 'todayonline3.csv')


def TextProcess(content):
    lettersOnly = re.sub("[^a-zA-Z]", " ", content)
    lowerCase = lettersOnly.lower()

    words = lowerCase.split()
    cachedstopwords = open(Paths.textPath + 'stopwords.txt').read()
    stopwords = cachedstopwords.split('\n')
    words = [w for w in words if w not in stopwords]

    # words = [PorterStemmer().stem(w) for w in words]

    words = [WordNetLemmatizer().lemmatize(w) for w in words]

    return " ".join(words)
