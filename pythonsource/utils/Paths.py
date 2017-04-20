import os


class Paths:
    def __init__(self):
        pass

    rcv1DataHome = 'E:\Anaconda\Anaconda\packages\data'
    textPath = os.path.dirname(os.getcwd()) + '\\text\\'

    pklDataPath = os.path.dirname(os.getcwd()) + '\\storeddata\\'
    keywordspath = os.path.dirname(os.getcwd()) + '\\keywords\\'
    imagespath = os.path.dirname(os.getcwd()) + '\\images\\'
    csvpath = os.path.dirname(os.getcwd()) + '\\csvs\\'
