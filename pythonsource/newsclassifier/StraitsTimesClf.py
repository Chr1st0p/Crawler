import pandas as pd
from pandas import DataFrame
from sklearn.datasets.base import Bunch
from utils.Paths import Paths
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, recall_score, f1_score, classification_report


def ProcessTrainSet():
    # unlabelCat = ['Defult', 'Top of the News']

    # remove nans
    dfs = pd.read_csv(Paths.csvpath + "straitstimes.csv").dropna()
    # trainData = dfs[(dfs['category'] != 'Defult') & (dfs['category'] != 'Top of the News')][['category', 'content']]
    # testData = dfs[(dfs['category'] == 'Defult') | (dfs['category'] == 'Top of the News')][['category', 'content']]
    trainData = dfs[(dfs['category'] != 'Defult')][['category', 'content']]
    testData = dfs[(dfs['category'] == 'Defult')][['category', 'content']]
    trainLen = len(trainData)
    print len(testData)

    Data = trainData.append(testData)

    le = preprocessing.LabelEncoder()
    label = le.fit_transform(Data['category'])
    print le.classes_
    dataSet = Bunch(data=Data['content'], target=label, target_names=le.classes_)

    count_vect = CountVectorizer()
    DataCount = count_vect.fit_transform(dataSet.data)

    tfidf_transformer = TfidfTransformer()
    DataTfIdf = tfidf_transformer.fit_transform(DataCount)

    X_train = DataTfIdf[:trainLen]
    X_test = DataTfIdf[trainLen:]
    Y_train = dataSet.target[:trainLen]

    clf = MultinomialNB().fit(X_train, Y_train)
    predictionTrain = clf.predict(X_train)

    joblib.dump(clf, Paths.pklDataPath + 'StraitsTimesClassifier.pkl')
    print classification_report(Y_train, predictionTrain, target_names=dataSet.target_names)
    prediction = clf.predict(X_test)
    df = DataFrame(prediction)
    df.to_csv(Paths.csvpath + 'prediction.csv')
