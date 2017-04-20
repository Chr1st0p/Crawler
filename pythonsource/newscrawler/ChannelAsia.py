from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import mysql.connector
from utils.Config import BackColors, DbConfig, RequestHeader
import multiprocessing
import re
from parsers.DateParser import ChannelAsiaDateParse


def start():
    # max page 2357
    for i in range(12, -1, -1):
        getHtml(i)
    AsiaNews.cnn.close()


def getHtml(iters):
    targeturl = AsiaNews.url + str(iters)
    print('Start Get ' + str(iters + 1) + 'th Page ChannelAsia News')
    html = requests.get(url=targeturl, headers=RequestHeader.browserHeader)
    soup = BeautifulSoup(html.text, 'lxml')
    # delete the div with class=panel-panel right,

    matchcontent = soup.find_all(name='div', attrs={'class', 'txt-box'}, limit=10)

    # separete the title, link, date, abstract;
    # print matchcontent[1]

    poolToday = multiprocessing.Pool(processes=10)
    if len(matchcontent) >= 10:
        for i in range(9, -1, -1):
            poolToday.apply_async(parseHtml, args=(iters, matchcontent[i]))
        poolToday.close()
        poolToday.join()
    # parseHtml(iters, matchcontent[i], i)
    else:
        poolToday = multiprocessing.Pool(processes=len(matchcontent))
        for i in range(len(matchcontent) - 1, -1, -1):
            poolToday.apply_async(parseHtml, args=(iters, matchcontent[i]))
        poolToday.close()
        poolToday.join()


def parseHtml(iters, match):
    matchlink = ''
    title = ''
    date = ''
    content = ''
    keyword = ''
    # noinspection PyBroadException
    try:
        matchlink = match.find(name='h2').find(name='a').get('href')
        link = 'http://www.channelnewsasia.com' + matchlink
    except:
        print(BackColors.WARNING + 'The ' + str(iters) + 'th Page ' + 'th link Error' + BackColors.ENDC)
        link = ''

    if matchlink:
        contentHtml = requests.get(url=link, headers=RequestHeader.browserHeader)
        contentSoup = BeautifulSoup(contentHtml.text, 'lxml')
        content = contentSoup.find(attrs={'name': 'description'})['content'] \
            .replace('\n', '')
        keyword = contentSoup.find(attrs={'name': 'news_keywords'})['content']

        title = contentSoup.find(attrs={'name': 'twitter:title'})['content']
        date = contentSoup.find(name='li', attrs={'class', 'news_posttime'}).get_text()
        date = ChannelAsiaDateParse(date)
    data = (iters, title, link, keyword, date, content)
    # print(data)
    if keyword:
        insertData(data)


def createTable():
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS channelaisadata (" \
                     "id       INT AUTO_INCREMENT PRIMARY KEY," \
                     "page     INT NOT NULL," \
                     "title    VARCHAR(1000) NOT NULL UNIQUE," \
                     "link     VARCHAR(1000) NOT NULL UNIQUE," \
                     "keyword     TEXT," \
                     "postdate DATE ," \
                     "content TEXT)"

    cursor = AsiaNews.cnn.cursor()
    try:
        cursor.execute(sqlCreateTable)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'create table channelaisa fails!{}'.format(e) + BackColors.ENDC)


def insertData(data):
    cursor = AsiaNews.cnn.cursor()
    sql_insert = 'INSERT INTO channelaisadata (page, title, link,keyword,postdate, content) VALUES (%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql_insert, data)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'insert data error!{}'.format(e) + BackColors.ENDC)
    finally:
        AsiaNews.cnn.commit()
        cursor.close()
        AsiaNews.cnn.close()


class AsiaNews:
    url = 'http://www.channelnewsasia.com/archives/3636/Singapore/months/latest/'
    cnn = mysql.connector.connect(**DbConfig.newsDataConfig)

    def __init__(self):
        # try:
        #     self.cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        # except mysql.connector.Error as e:
        #     print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        createTable()
