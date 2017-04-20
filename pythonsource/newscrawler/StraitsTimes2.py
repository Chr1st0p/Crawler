from __future__ import print_function
import requests
import multiprocessing
from bs4 import BeautifulSoup
import mysql.connector
from utils.Config import BackColors, DbConfig, RequestHeader
from parsers.DateParser import StraitsTimesDateParse
import re

proxies = {
    'http://119.5.0.6:808/',
    'http://106.46.136.85:808/',
    'http://119.5.0.14:808/',
    'http://106.46.136.200:808/',
    'http://106.46.136.24:808/',
    'http://106.46.136.108:808/',
}


def main():
    for i in xrange(1, -1, -1):
        getHtml(i)
    StraitsTimesNews.cnn.close()


def getHtml(iters):
    if iters == 0:
        targeturl = StraitsTimesNews.url
    else:
        targeturl = StraitsTimesNews.url + StraitsTimesNews.pageDownStr + str(iters)
    print('Start Get ' + str(iters) + 'th Page StraitsTimes News')
    html = requests.get(url=targeturl, headers=RequestHeader.browserHeader)
    soup = BeautifulSoup(html.text, 'lxml')

    matchTittleLink = soup.find_all(name='div', attrs={'class', 'media-body '})
    matchDate = soup.find_all(name='div', attrs={'class', 'media-footer'})
    # if len(matchTittleLink) == 0:
    #     pool2 = multiprocessing.Pool(processes=25)
    # else:
    pool2 = multiprocessing.Pool(processes=27)
    # separete the title, link, date
    for i in xrange(len(matchDate) - 1, -1, -1):
        # pool.map()
        pool2.apply_async(parseHtml, args=(iters, matchTittleLink[i], matchDate[i], i))
        # parseHtml(iters, matchTittleLink[i], matchDate[i], i)
        # self.paraseNews(matchTittleLink[i], matchDate[i])
    pool2.close()
    pool2.join()
    # print 'get ' + str(iters) + 'th page done'


def parseHtml(iters, matchTL, matchD, i):
    # news title, link, date,
    # noinspection PyBroadException
    # print 'start'
    try:
        title = matchTL.find(name='a').get_text()
    except:
        print(BackColors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th title Error' + BackColors.ENDC)
        title = ''
    # noinspection PyBroadException
    try:
        link = 'http://www.straitstimes.com' + matchTL.find(name='a').get('href')
    except:
        print(BackColors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + BackColors.ENDC)
        link = ''
        # noinspection PyBroadException
    if link == '':
        content = ''
        keyword = ''
        category = ''
        date = ''
    else:
        # noinspection PyBroadException
        keyword, content, category, date = parseContentKeyword(link)

    d = StraitsTimesDateParse(date)
    if not category.strip():
        category = 'Defult'
    if keyword.strip():
        data = (iters, title, link, d, category, keyword, content)
        insertData(data)


def insertData(data):
    cursor = StraitsTimesNews.cnn.cursor()
    sql_insert = 'INSERT INTO StraitsTimesNewData (page, title, link, postdate,category,keyword,content) ' \
                 'VALUES (%s, %s, %s, %s,%s,%s,%s)'
    try:
        cursor.execute(sql_insert, data)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'insert data error!{}'.format(e) + BackColors.ENDC)
    finally:
        StraitsTimesNews.cnn.commit()
        cursor.close()
        StraitsTimesNews.cnn.close()


def parseContentKeyword(newsurl):
    html = requests.get(url=newsurl, headers=RequestHeader.browserHeader)
    category = ''
    date = ''
    try:
        vardata = re.search(r"var _data = {((?:\s|.)+?)\}", html.text)
    except:
        print("Keyword or category match Error")
        return '', '', '', ''
    if vardata.group(0):
        try:
            keyword = re.findall(r".*\"keyword\":\"(.*?)\"", vardata.group(0))
            # print(keyword)
        except:
            keyword = ''
        try:
            category = re.findall(".*\"printcat\":\"(.*?)\"", vardata.group(0))
            # print(category)
        except:
            category = ''
        try:
            date = re.findall(".*\"pubdate\":\"(.*?)\"", vardata.group(0))
        except:
            date = ''
    content = ''
    soup = BeautifulSoup(html.text, 'lxml')
    matchContent = soup.find_all(name='p')
    for i in range(len(matchContent) - 5):
        content += matchContent[i].get_text()
    return keyword[0], content, category[0], date[0]


def createTable():
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS StraitsTimesNewData (" \
                     "id       INT AUTO_INCREMENT PRIMARY KEY," \
                     "page     INT NOT NULL," \
                     "title    VARCHAR(1024) UNIQUE," \
                     "link     TEXT," \
                     "postdate DATE," \
                     "category TEXT," \
                     "keyword TEXT," \
                     "content TEXT)"
    cursor = StraitsTimesNews.cnn.cursor()
    try:
        cursor.execute(sqlCreateTable)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'create table StraitsTimesData fails!{}'.format(e) + BackColors.ENDC)


class StraitsTimesNews:
    cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
    url = 'http://www.straitstimes.com/singapore/latest'
    pageDownStr = '?page='

    def __init__(self):
        createTable()
