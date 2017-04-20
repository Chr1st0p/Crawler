class BackColors:
    def __init__(self):
        pass

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DbConfig:
    def __init__(self):
        pass

    newsDataConfig = {'host': '127.0.0.1',
                      'user': 'root',
                      'password': 'qwerty123456',
                      'port': '3306',
                      'database': 'newsdata',
                      'charset': 'utf8'
                      }

    socialMediaConfig = {'host': '127.0.0.1',
                         'user': 'root',
                         'password': 'qwerty123456',
                         'port': '3306',
                         'database': 'socialmedia',
                         'charset': 'utf8'
                         }


class RequestHeader:
    def __init__(self):
        pass

    browserHeader = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 "
                      "Safari/537.36"}
