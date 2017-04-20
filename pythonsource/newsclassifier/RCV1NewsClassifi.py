from sklearn.datasets import fetch_rcv1
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, recall_score, f1_score
import pandas as pd
import numpy as np
from utils.Paths import Paths

trainingnum = 600000

vocabulary = joblib.load(Paths.pklDataPath + 'rcv1vocabulary.pkl')
clf = joblib.load(Paths.pklDataPath + 'NBClassifier.pkl')


def convertdict():
    dataVocabulary = pd.read_csv(Paths.textPath + 'rcv1vocabulary.txt', sep=" ", header=None)
    vocabular = dict()
    for word, did in zip(dataVocabulary[0], dataVocabulary[1]):
        vocabular[word] = did - 1
    joblib.dump(vocabular, Paths.pklDataPath + 'rcv1vocabulary.pkl')


def train():
    convertdict()
    print 'Start training a multiclass Naive Bayesian Classifier...' + str(trainingnum) + ' training data is used.'
    rcv1 = fetch_rcv1(data_home=Paths.rcv1DataHome, random_state=1)

    X_train = rcv1.data[:trainingnum]
    Y_train = rcv1.target[:trainingnum]

    X_test = rcv1.data[trainingnum:]
    Y_test = rcv1.target[trainingnum:]
    multiClassClf = OneVsRestClassifier(MultinomialNB()).fit(X_train, Y_train)

    joblib.dump(multiClassClf, Paths.pklDataPath + 'NBClassifier.pkl')
    predictionTrain = multiClassClf.predict(X_train)
    print 'Train accuracy:'
    print accuracy_score(predictionTrain.toarray(), Y_train.toarray())
    print 'Train Recall:'
    print recall_score(predictionTrain.toarray(), Y_train.toarray(), average='macro')
    print 'F1 Score:'
    print f1_score(predictionTrain.toarray(), Y_train.toarray(), average='macro')
    prediction = multiClassClf.predict(X_test)
    print 'Accuracy is: ',
    print accuracy_score(prediction.toarray(), Y_test.toarray())
    print 'F1 Score:'
    print f1_score(prediction.toarray(), Y_test.toarray(), average='macro')


def predict(news):
    text = news
    vectorizer = CountVectorizer(stop_words='english', vocabulary=vocabulary)
    IDFTransformer = TfidfTransformer(use_idf=True)
    X = vectorizer.fit_transform(text)
    doc = IDFTransformer.fit_transform(X)

    print "pred"
    prediction = clf.predict(doc)
    print prediction
    print prediction.toarray()[0]
    print np.where(prediction.toarray()[0] == 1)[0]
