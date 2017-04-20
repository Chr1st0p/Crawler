from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import mysql.connector
from utils.Config import BackColors, DbConfig, RequestHeader
import multiprocessing
from parsers.DateParser import MustShareNewsDateParse
from textrank import extractKeyphrases, extractSentences
import re
from utils.Paths import Paths


def start():
    for i in range(5, 0, -1):
        for cat in MustShareNews.categoryList:
            getHtml(i, cat)
    MustShareNews.cnn.close()


def getHtml(iters, category):
    if iters == 1:
        targeturl = MustShareNews.url + category + "/"
    else:
        targeturl = MustShareNews.url + category + "/" + MustShareNews.pageDownStr + '/' + str(iters) + '/'
    print('Start Get ' + str(iters) + 'th Page MustShareNews ' + category + " part")
    html = requests.get(url=targeturl, headers=RequestHeader.browserHeader)
    soup = BeautifulSoup(html.text, 'lxml')

    # match the news div,the first one is the brief news which is useless,only 2-10 are the news;
    matchcontent = soup.find_all(name='div', attrs={'class': 'read-more'}, limit=10)

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
        print(len(matchcontent))
        if len(matchcontent) > 0:
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
    keyword = ''
    try:
        matchlink = match.find(name='a').get('href')
        link = matchlink
    except:
        print(BackColors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + BackColors.ENDC)
        link = ''
    if matchlink:
        contentHtml = requests.get(url=link, headers=RequestHeader.browserHeader)
        contentSoup = BeautifulSoup(contentHtml.text, 'lxml')
        title = contentSoup.find_all(attrs={"property": "og:title"})[0]['content']
        date = contentSoup.find_all(attrs={"property": 'article:published_time'})[0]["content"]
        date = MustShareNewsDateParse(date)

        contents = contentSoup.find(name='div', attrs={"class": "post-content description "})
        texts = contents.find_all(name='p')
        for t in texts:
            content = content + t.get_text()

        tagDiv = contentSoup.find(name='div', attrs={"class": "tagcloud"})
        keywords = tagDiv.find_all(name='a')
        for k in keywords:
            keyword = keyword + k.get_text() + " "

    # content = contentSoup.find(name='div', attrs={'class', 'post-content'}).get_text()
    #     keywords = extractSentences(content)
    #     keywords = extractKeyphrases(keywords)
    #
    #     lettersOnly = re.sub("[^a-zA-Z]", " ", " ".join(keywords))
    #     lowerCase = lettersOnly.lower()
    #     words = lowerCase.split()
    #     cachedstopwords = open(Paths.textPath + 'stopwords.txt').read()
    #     stopwords = cachedstopwords.split('\n')
    #     words = [w for w in words if w not in stopwords]
    #     keyword = " ".join(words)
    data = (iters, str(title), str(link), str(category), str(keyword), date, str(content))

    if matchlink and keyword and title and content:
        insertData(data)


def createTable():
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS mustsharenews (" \
                     "id       INT AUTO_INCREMENT PRIMARY KEY," \
                     "page     INT NOT NULL," \
                     "title    VARCHAR(1000) NOT NULL," \
                     "link     VARCHAR(1000) NOT NULL UNIQUE," \
                     "category     TEXT," \
                     "keyword     TEXT," \
                     "postdate DATE, " \
                     "content TEXT)"

    cursor = MustShareNews.cnn.cursor()
    try:
        cursor.execute(sqlCreateTable)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'create table todayonline fails!{}'.format(e) + BackColors.ENDC)


def insertData(data):
    cursor = MustShareNews.cnn.cursor()
    sql_insert = 'INSERT INTO mustsharenews (page, title, link, category,keyword,postdate, content) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql_insert, data)
    except mysql.connector.Error as e:
        print(BackColors.WARNING + 'insert data error!{}'.format(e) + BackColors.ENDC)
    finally:
        MustShareNews.cnn.commit()
        cursor.close()
        MustShareNews.cnn.close()


class MustShareNews:
    url = 'https://mustsharenews.com/category/'
    categoryList = ['currentaffairs', 'people', 'lifestyle', 'inspiration', 'lifestyle']
    pageDownStr = 'page'
    cnn = mysql.connector.connect(**DbConfig.socialMediaConfig)

    def __init__(self):
        # try:
        #     self.cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        # except mysql.connector.Error as e:
        #     print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        createTable()
