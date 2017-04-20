from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import mysql.connector
from utils.Config import BackColors, DbConfig, RequestHeader
import multiprocessing
import re
from parsers.DateParser import TodayOnlineDateParse


def start():
    # max page 2357
    for i in range(103, -1, -1):
        getHtml(i)
    TodayNews.cnn.close()


def getHtml(iters):
    if iters == 0:
        targeturl = TodayNews.url
    else:
        targeturl = TodayNews.url + TodayNews.pageDownStr + str(iters)
    print('Start Get ' + str(iters) + 'th Page TodayOnline News')
    html = requests.get(url=targeturl, headers=RequestHeader.browserHeader)
    soup = BeautifulSoup(html.text, 'lxml')
    # delete the div with class=panel-panel right,
    # without this step, the result in next step will be class=panel-panel right + class=right;
    for div in soup.find_all("div", {'class': 'panel-panel right'}):
        div.decompose()

    # match the news div,the first one is the brief news which is useless,only 2-10 are the news;
    matchcontent = soup.find_all(name='div', attrs={'class', 'right'}, limit=11)

    # separete the title, link, date, abstract;
    # print matchcontent[1]
    if len(matchcontent) >= 11:
        poolToday = multiprocessing.Pool(processes=10)
        for i in range(10, 0, -1):
            poolToday.apply_async(parseHtml, args=(iters, matchcontent[i], i))
        poolToday.close()
        poolToday.join()
    # parseHtml(iters, matchcontent[i], i)
    else:
        poolToday = multiprocessing.Pool(processes=len(matchcontent))
        for i in range(len(matchcontent) - 1, -1, -1):
            poolToday.apply_async(parseHtml, args=(iters, matchcontent[i], i))
        poolToday.close()
        poolToday.join()


def parseHtml(iters, match, i):
    matchlink = ''
    title = ''
    date = ''
    content = ''
    keyword = ''
    category = ''
    # noinspection PyBroadException
    try:
        matchlink = match.find(name='h2').find(name='a').get('href')
        link = 'http://www.todayonline.com' + matchlink
    except:
        print(BackColors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + BackColors.ENDC)
        link = ''

    if matchlink:
        contentHtml = requests.get(url=link, headers=RequestHeader.browserHeader)
        contentSoup = BeautifulSoup(contentHtml.text, 'lxml')
        content = contentSoup.find_all(attrs={'property': 'og:description'})[0]['content'].encode('utf-8') \
            .replace('\n', '').replace('SINGAPORE', '')

        title = contentSoup.find_all(attrs={'property': 'twitter:title'})[0]['content']

        date = re.findall(r".*\"contentpublishdate\" :\"(.*?)\"", contentHtml.text)

        date = TodayOnlineDateParse(date[0])

        keyCat = re.findall(r".*googletag.pubads\(\).setTargeting\(\"TodayKW\", \[\"(.*?)\"\]\)", contentHtml.text)
        keyCatList = keyCat[0].replace('"', ' ').strip().split(',')
        if len(keyCatList) > 2:
            for i in xrange(len(keyCatList) - 1):
                category += (keyCatList[i] + ',')
            keyword = keyCatList[len(keyCatList)]
        else:
            category = keyCatList[0]
            keyword = keyCatList[1]
    data = (iters, title, link, category, keyword, date, content)

    if title and matchlink and date and ('TODAY\'s morning brief' not in title) and ('todays-brief' not in link):
        insertData(data)


def createTable():
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS todayonlinenewdata (" \
                     "id       INT AUTO_INCREMENT PRIMARY KEY," \
                     "page     INT NOT NULL," \
                     "title    VARCHAR(1000) NOT NULL UNIQUE," \
                     "link     VARCHAR(1000) NOT NULL UNIQUE," \
                     "category     TEXT," \
                     "keyword     TEXT," \
                     "postdate DATE, " \
                     "content TEXT)"

    cursor = TodayNews.cnn.cursor()
    try:
        cursor.execute(sqlCreateTable)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'create table todayonline fails!{}'.format(e) + BackColors.ENDC)


def insertData(data):
    cursor = TodayNews.cnn.cursor()
    sql_insert = 'INSERT INTO todayonlinenewdata (page, title, link, category,keyword,postdate, content) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql_insert, data)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'insert data error!{}'.format(e) + BackColors.ENDC)
    finally:
        TodayNews.cnn.commit()
        cursor.close()
        TodayNews.cnn.close()


class TodayNews:
    url = 'http://www.todayonline.com/singapore'
    pageDownStr = '?page='
    cnn = mysql.connector.connect(**DbConfig.newsDataConfig)

    def __init__(self):
        # try:
        #     self.cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        # except mysql.connector.Error as e:
        #     print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        createTable()
