from wordcloud import WordCloud
import re
from utils.Paths import Paths


def DrawStraitsTimesCloud(year, month):
    cachedstopwords = open(Paths.textPath + 'stopwords.txt').read()
    stopwords = cachedstopwords.split('\n')
    f = open(Paths.keywordspath + str(year) + str(month) + '.txt', 'r')
    data = f.read()
    tokens = re.findall(r"[\w']+", data)
    lowerToken = [word.lower() for word in tokens]

    filteredToken = [word for word in lowerToken if word not in stopwords]
    w = WordCloud().process_text(' '.join(filteredToken))
    w = sorted(w.items(), reverse=True, key=lambda x: x[1])
    print w
    # w = WordCloud(max_words=50, width=750, height=650).generate(' '.join(filteredToken))
    # w.to_file(Paths.imagespath + str(year) + str(month) + ".png")
    # image = w.to_image()
    # image.show()
