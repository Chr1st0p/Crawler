from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import mysql.connector
from utils.Config import BackColors, DbConfig, RequestHeader
import multiprocessing
from parsers.DateParser import MotherShipDateParse
from textrank import extractKeyphrases, extractSentences
import re
from utils.Paths import Paths
from summa import keywords


def start():
    for i in range(2, 0, -1):
        for cat in MotherShip.categoryList:
            getHtml(i, cat)
    MotherShip.cnn.close()


def getHtml(iters, category):
    if iters == 0:
        targeturl = MotherShip.url + category + "/"
    else:
        targeturl = MotherShip.url + category + "/" + MotherShip.pageDownStr + str(iters) + '/'
    print('Start Get ' + str(iters) + 'th Page Mothership ' + category + " part")
    html = requests.get(url=targeturl, headers=RequestHeader.browserHeader)
    soup = BeautifulSoup(html.text, 'lxml')

    # match the news div,the first one is the brief news which is useless,only 2-10 are the news;
    matchcontent = soup.find_all(name='div', attrs={'class', 'post-desc'}, limit=15)

    # separete the title, link, date, abstract;
    # print matchcontent[1]
    if len(matchcontent) >= 15:
        poolToday = multiprocessing.Pool(processes=15)
        for i in range(14, -1, -1):
            poolToday.apply_async(parseHtml, args=(iters, category, matchcontent[i], i))
        poolToday.close()
        poolToday.join()
    # parseHtml(iters, matchcontent[i], i)
    else:
        poolToday = multiprocessing.Pool(processes=len(matchcontent))
        for i in range(len(matchcontent) - 1, -1, -1):
            poolToday.apply_async(parseHtml, args=(iters, category, matchcontent[i], i))
        poolToday.close()
        poolToday.join()


def parseHtml(iters, category, match, i):
    matchlink = ''
    title = ''
    date = ''
    content = ''
    key = ''
    try:
        matchlink = match.find(name='h3').find(name='a').get('href')
        link = matchlink
    except:
        print(BackColors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + BackColors.ENDC)
        link = ''
    try:
        date = match.find(name='div', attrs={'class', 'post-date'}).get_text()
    except:
        date = ""
    d = MotherShipDateParse(date)

    if matchlink:
        contentHtml = requests.get(url=link, headers=RequestHeader.browserHeader)
        contentSoup = BeautifulSoup(contentHtml.text, 'lxml')
        title = contentSoup.find(name='h1', attrs={'class', 'content-title'}).get_text()
        content = contentSoup.find(name='div', attrs={'class', 'post-content'}).get_text()

        lettersOnly = re.sub("[^a-zA-Z]", " ", content)
        lowerCase = lettersOnly.lower()
        words = lowerCase.split()
        cachedstopwords = open(Paths.textPath + 'stopwords.txt').read()
        stopwords = cachedstopwords.split('\n')
        words = [w for w in words if w not in stopwords]
        contents = " ".join(words)

        key = keywords.keywords(contents)
        # key = extractKeyphrases(contents)
        # keywords = extractSentences(content)
        # keywords = extractKeyphrases(keywords)
        key = key.replace("\n", " ")
        d = MotherShipDateParse(date)

    # data = (title, link, category, key, d, content)
    #
    # if matchlink and key and title and content:
    #     insertData(data)

    data = (str(title), str(link), str(category), str(key), str(d), str(lettersOnly))

    if matchlink and key and title and content:
        insertData(data)


def createTable():
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS mothership (" \
                     "id       INT AUTO_INCREMENT PRIMARY KEY," \
                     "title    VARCHAR(1000) NOT NULL," \
                     "link     VARCHAR(1000) NOT NULL UNIQUE," \
                     "category     TEXT," \
                     "keyword     TEXT," \
                     "postdate DATE, " \
                     "content TEXT)"

    cursor = MotherShip.cnn.cursor()
    try:
        cursor.execute(sqlCreateTable)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'create table todayonline fails!{}'.format(e) + BackColors.ENDC)


def insertData(data):
    cursor = MotherShip.cnn.cursor()
    sql_insert = 'INSERT INTO mothership (title, link, category,keyword,postdate, content) VALUES (%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql_insert, data)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'insert data error!{}'.format(e) + BackColors.ENDC)
    finally:
        MotherShip.cnn.commit()
        cursor.close()
        MotherShip.cnn.close()


class MotherShip:
    url = 'http://mothership.sg/category/'
    categoryList = ['news', 'humour', 'perspectives', 'community', 'lifestyle']
    pageDownStr = 'page'
    cnn = mysql.connector.connect(**DbConfig.socialMediaConfig)

    def __init__(self):
        # try:
        #     self.cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        # except mysql.connector.Error as e:
        #     print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        createTable()
