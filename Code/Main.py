import csv
from sklearn.tree import DecisionTreeClassifier
import data_helpers
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import  TfidfTransformer,TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.svm import LinearSVC, SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, f1_score, classification_report
from sklearn.model_selection import KFold, train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from time import time
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

def benchmark(clf,X_train,y_train,X_test,y_test):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)
    clf_descr = str(clf).split('(')[0]
    print (classification_report(y_test, pred))
    return clf_descr, score, train_time, test_time

for i in range(2,6):

    print("Loading data "+str(i)+" classes ......")
    X,Y = data_helpers.load_data_and_labels(i)
    print("X shape is {}".format(np.shape(X)))
    print("Y shape is {}".format(np.shape(Y)))

    # Using TfidfVectorizer ,which equvelent to use CountVectorizer and then tfidf_trasformation
    vectorizer = TfidfVectorizer(encoding='latin1',stop_words='english',ngram_range=(1,2))
    X = vectorizer.fit_transform(X)

    print("X shape is {}".format(np.shape(X)))

    x_train, x_test, label_train, label_test =train_test_split(X, Y, test_size=0.1)

    results = []
    for clf, name in (
            (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
            (Perceptron(n_iter=50,n_jobs=-1), "Perceptron"),
            (PassiveAggressiveClassifier(n_iter=50), "Passive-Aggressive"),
            (KNeighborsClassifier(n_neighbors=10), "kNN"),
            (RandomForestClassifier(n_estimators=100), "Random forest")):
        print('=' * 80)
        print(name)
        results.append(benchmark(clf,x_train,label_train,x_test,label_test))

    for penalty in ["l2", "l1"]:
        print('=' * 80)
        print("%s penalty" % penalty.upper())
        # Train Liblinear model
        results.append(benchmark(LinearSVC(loss='l2', penalty=penalty,
                                            dual=False, tol=1e-3),x_train,label_train,x_test,label_test))

    # Train SGD model
    results.append(benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                               penalty=penalty),x_train,label_train,x_test,label_test))

    # Train SGD with Elastic Net penalty
    print('=' * 80)
    print("Elastic-Net penalty")
    results.append(benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                        penalty="elasticnet"),x_train,label_train,x_test,label_test))

    # Train NearestCentroid without threshold
    print('=' * 80)
    print("NearestCentroid (aka Rocchio classifier)")
    results.append(benchmark(NearestCentroid(),x_train,label_train,x_test,label_test))

    # Train sparse Naive Bayes classifiers
    print('=' * 80)
    print("Naive Bayes")
    results.append(benchmark(MultinomialNB(alpha=.01),x_train,label_train,x_test,label_test))
    results.append(benchmark(BernoulliNB(alpha=.01),x_train,label_train,x_test,label_test))
