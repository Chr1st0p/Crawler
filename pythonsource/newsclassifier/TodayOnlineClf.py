import pandas as pd
from sklearn.datasets.base import Bunch
from utils.Paths import Paths
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, recall_score, f1_score, classification_report, precision_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def ShowResult(actual, predict):
    precision = precision_score(actual, predict, average='weighted')
    recall = recall_score(actual, predict, average='weighted')
    f1 = f1_score(actual, predict, average='weighted')

    print 'Predict info'
    print 'Precision: {0:.3f}'.format(precision)
    print 'Recall: {0:.3f}'.format(recall)
    print 'F1-score: {0:.3f}'.format(f1)


def TrainClassifier():
    dfs = pd.read_csv(Paths.csvpath + 'todayonline2.csv')

    dataset = dfs[(dfs['category'] != 'Defaut')][['category', 'content']]

    predictedset = dfs[(dfs['category'] == 'Defaut')][['category', 'content']]

    le = preprocessing.LabelEncoder()
    label = le.fit_transform(dataset['category'])
    print le.classes_

    dataSet = Bunch(data=dataset['content'], target=label, target_names=le.classes_)

    count_vect = CountVectorizer()
    DataCount = count_vect.fit_transform(dataSet.data)

    tfidf_transformer = TfidfTransformer()
    DataTfIdf = tfidf_transformer.fit_transform(DataCount)

    X_train, X_test, Y_train, Y_test = train_test_split(DataTfIdf, dataSet.target, random_state=0)

    print "NB Report"
    clf1 = MultinomialNB().fit(X_train, Y_train)
    # predictionNB = clf1.predict(X_train)
    # ShowResult(Y_train, predictionNB)
    # print classification_report(Y_train, predictionNB, target_names=dataSet.target_names)
    testNB = clf1.predict(X_test)
    ShowResult(Y_test,testNB)
    print classification_report(Y_test,testNB,target_names=dataSet.target_names)

    # print "KNN Report"
    # clf2 = KNeighborsClassifier(n_neighbors=5)
    # clf2.fit(X_train, Y_train)
    # predictionKNN = clf2.predict(X_train)
    # ShowResult(Y_train, predictionKNN)
    # print classification_report(Y_train, predictionKNN, target_names=dataSet.target_names)


    print "SVM Report"
    clf3 = SVC(kernel='linear')
    clf3.fit(X_train, Y_train)
    # predictionSVM = clf3.predict(X_train)
    # ShowResult(Y_train, predictionSVM)
    # print classification_report(Y_train, predictionSVM, target_names=dataSet.target_names)
    testSVM = clf3.predict(X_test)
    ShowResult(Y_test, testSVM)
    print classification_report(Y_test, testSVM, target_names=dataSet.target_names)

