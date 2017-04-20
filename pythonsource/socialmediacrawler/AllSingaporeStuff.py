from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import mysql.connector
from utils.Config import BackColors, DbConfig, RequestHeader
from utils.Paths import Paths
import multiprocessing
from parsers.DateParser import AllSingaporeStuffDateParse
from textrank import extractKeyphrases, extractSentences
import re
from summa import keywords


def start():
    for i in range(10, -1, -1):
        for cat in AllSingaoreStuff.categoryList:
            getHtml(i, cat)
    AllSingaoreStuff.cnn.close()


def getHtml(iters, category):
    if iters == 0:
        targeturl = AllSingaoreStuff.url + category + "/"
    else:
        targeturl = AllSingaoreStuff.url + category + AllSingaoreStuff.pageDownStr + str(iters)
    print('Start Get ' + str(iters) + 'th Page All Singapore Stuff ' + category + " part")
    html = requests.get(url=targeturl, headers=RequestHeader.browserHeader)
    soup = BeautifulSoup(html.text, 'lxml')

    # match the news div,the first one is the brief news which is useless,only 2-10 are the news;
    matchcontent = soup.find_all(name='h1', attrs={'class', 'node-title'}, limit=10)

    # separete the title, link, date, abstract;
    # print matchcontent[1]
    if len(matchcontent) >= 10:
        poolToday = multiprocessing.Pool(processes=10)
        for i in range(9, -1, -1):
            poolToday.apply_async(parseHtml, args=(iters, category, matchcontent[i], i))
        poolToday.close()
        poolToday.join()
    # parseHtml(iters, matchcontent[i], i)
    else:
        if len(matchcontent) > 0:
            poolToday = multiprocessing.Pool(processes=len(matchcontent))
            for i in range(len(matchcontent) - 1, -1, -1):
                poolToday.apply_async(parseHtml, args=(iters, category, matchcontent[i], i))
            poolToday.close()
            poolToday.join()


def parseHtml(iters, category, match, i):
    matchlink = ''
    title = ''
    key = ''
    content = ''
    try:
        matchlink = match.find(name='a').get('href')
        link = 'https://www.allsingaporestuff.com' + matchlink
    except:
        print(BackColors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + BackColors.ENDC)
        link = ''
    if matchlink:
        contentHtml = requests.get(url=link, headers=RequestHeader.browserHeader)
        contentSoup = BeautifulSoup(contentHtml.text, 'lxml')
        date = contentSoup.find_all(name='span', attrs={'property': 'dc:date dc:created'})[0]['content']

        title = contentSoup.find_all(attrs={'property': 'og:title'})[0]['content']
        content = contentSoup.find_all(attrs={'name': 'twitter:description'})[0]['content']
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
        d = AllSingaporeStuffDateParse(date)

    data = (iters, title, link, category, key, d, content)

    if matchlink and key and title and content:
        insertData(data)


def createTable():
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS allsingaporestuff (" \
                     "id       INT AUTO_INCREMENT PRIMARY KEY," \
                     "page     INT NOT NULL," \
                     "title    VARCHAR(1000) NOT NULL," \
                     "link     VARCHAR(1000) NOT NULL UNIQUE," \
                     "category     TEXT," \
                     "keyword     TEXT," \
                     "postdate DATE, " \
                     "content TEXT)"

    cursor = AllSingaoreStuff.cnn.cursor()
    try:
        cursor.execute(sqlCreateTable)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'create table allsingaporestuff fails!{}'.format(e) + BackColors.ENDC)


def insertData(data):
    cursor = AllSingaoreStuff.cnn.cursor()
    sql_insert = 'INSERT INTO allsingaporestuff (page, title, link, category,keyword,postdate, content) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql_insert, data)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'insert data error!{}'.format(e) + BackColors.ENDC)
    finally:
        AllSingaoreStuff.cnn.commit()
        cursor.close()
        AllSingaoreStuff.cnn.close()


class AllSingaoreStuff:
    url = 'https://www.allsingaporestuff.com/articles/'
    categoryList = ['news', 'editorials', 'alternatives', 'complaints', 'lifestyle', 'entertainment', 'sports']
    pageDownStr = '?page='
    cnn = mysql.connector.connect(**DbConfig.socialMediaConfig)

    def __init__(self):
        # try:
        #     self.cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        # except mysql.connector.Error as e:
        #     print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        createTable()
