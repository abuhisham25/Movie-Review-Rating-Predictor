import numpy as np
import pandas
import csv
from sklearn.tree import DecisionTreeClassifier
import data_helpers
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
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
# from __future__ import print_function

import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_20newsgroups
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
from sklearn.utils import shuffle

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
    # scaler = StandardScaler()
    t0 = time()
    # clf2 = Pipeline([('scaler', scaler), ('clf', clf)])
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
    return clf_descr, score, train_time, test_time


print("Loading data ......")
X,Y = data_helpers.load_data_and_labels("", "")
X, Y, = shuffle(X, Y)
print("X shape is {}".format(np.shape(X)))
print("Y shape is {}".format(np.shape(Y)))
# print(str(X[0]))
print("================================")
# print(str(X[1]))
vectorizer = TfidfVectorizer(encoding='latin1',stop_words='english')
X = vectorizer.fit_transform(X)
# scaler = preprocessing.StandardScaler(with_mean=False).fit(X1)
# X = scaler.transform(X1)
print("X shape is {}".format(np.shape(X)))
# ngram_range=(1,2)
# bow_transformer = CountVectorizer().fit(X)
# print("vocabulary length after CountVectorizer is {}".format(len(bow_transformer.vocabulary_)))
# text_bow = bow_transformer.transform(X)
# print("length know is "+str(np.shape(text_bow)))
# text_tfidf = TfidfTransformer().fit_transform(text_bow)
# print("vocabulary length after tfidf "+str(np.shape(text_tfidf)))


x_train, x_test, label_train, label_test =train_test_split(X, Y, test_size=0.2)

# benchmark(SVC(),x_train,label_train,x_test,label_test)
# benchmark(MultinomialNB, parameters, x_train,label_train,x_test,label_test)

results = []


####  (RandomForestClassifier(n_estimators=100), "Random forest"))

for clf, name in (
        (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
        (Perceptron(n_iter=50), "Perceptron"),
        (PassiveAggressiveClassifier(n_iter=50), "Passive-Aggressive"),
        (KNeighborsClassifier(n_neighbors=10), "kNN")):
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

print('=' * 80)
print("LinearSVC with L1-based feature selection")
# The smaller C, the stronger the regularization.
# The more regularization, the more sparsity.
results.append(benchmark(Pipeline([
  ('feature_selection', LinearSVC(penalty="l1", dual=False, tol=1e-3),x_train,label_train,x_test,label_test),
  ('classification', LinearSVC(),x_train,label_train,x_test,label_test)
])))

# # make some plots

# indices = np.arange(len(results))

# results = [[x[i] for x in results] for i in range(4)]

# clf_names, score, training_time, test_time = results
# training_time = np.array(training_time) / np.max(training_time)
# test_time = np.array(test_time) / np.max(test_time)

# plt.figure(figsize=(12, 8))
# plt.title("Score")
# plt.barh(indices, score, .2, label="score", color='navy')
# plt.barh(indices + .3, training_time, .2, label="training time",
#          color='c')
# plt.barh(indices + .6, test_time, .2, label="test time", color='darkorange')
# plt.yticks(())
# plt.legend(loc='best')
# plt.subplots_adjust(left=.25)
# plt.subplots_adjust(top=.95)
# plt.subplots_adjust(bottom=.05)

# for i, c in zip(indices, clf_names):
#     plt.text(-.3, i, c)

# plt.show()
# print("all data length is {}".format(len(Y)))
# print("train data length is {}".format(len(x_train)))
# print("test data length is {}".format(len(x_test)))

# print(str(label_test[:50]))
# x_train = x_train[0:int(len(x_train)/2)]
# label_train = label_train[0:int(len(label_train)/2)]

# pipeline = Pipeline([
#     ('bow', CountVectorizer()),  # strings to token integer counts
#     ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
#     ('classifier', KNeighborsClassifier())  # train on TF-IDF vectors w/ Naive Bayes classifier
# ])

# scores = cross_val_score(pipeline,  # steps to convert raw messages into models
#                          x_train,  # training data
#                          label_train,  # training labels
#                          cv=10,  # split data randomly into 10 parts: 9 for training, 1 for scoring
#                          scoring='accuracy',  # which scoring metric?
#                          n_jobs=-1,  # -1 = use all cores = faster
#                          )
# print(scores)

# params = {
#     'tfidf__use_idf': (True, False),
# }

# grid = GridSearchCV(
#     pipeline,  # pipeline from above
#     params,  # parameters to tune via cross validation
#     refit=True,  # fit using all available data at the end, on the best found param combination
#     n_jobs=-1,  # number of cores to use for parallelization; -1 for "all cores"
#     scoring='accuracy',  # what score are we optimizing?
#     cv=StratifiedKFold(n_splits=5),  # what type of cross validation to use
# )

# nb_detector = grid.fit(msg_train, label_train)
# report(nb_detector.cv_results_)
# print("testing the estimator MultinomialNB ")
# predictions = grid.predict(msg_test)
# print(classification_report(label_test, predictions))
# print(grid.score(msg_test, label_test))



# # print("============================================== level 2 with n-grams and SVC classifier =============")

# pipeline_svm = Pipeline([
#     ('bow', CountVectorizer()),
#     ('tfidf', TfidfTransformer()),
#     ('classifier', SVC()),  # <== change here
# ])
# param_svm = {
# 	'bow__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams or trigram}
# 	'classifier__kernel': ['linear'],
#  # {'classifier__C': [1, 10, 100, 1000], 'classifier__gamma': [0.001, 0.0001], 'classifier__kernel': ['rbf']},
# }

# grid_svm = GridSearchCV(
#     pipeline_svm,  # pipeline from above
#     param_grid=param_svm,  # parameters to tune via cross validation
#     refit=True,  # fit using all data, on the best detected classifier
#     n_jobs=-1,  # number of cores to use for parallelization; -1 for "all cores"
#     scoring='accuracy',  # what score are we optimizing?
#     cv=StratifiedKFold(n_splits=5),  # what type of cross validation to use
# )

# svm_detector = grid_svm.fit(x_train, label_train) # find the best combination from param_svm
# report(svm_detector.cv_results_)
# print("testing the estimator SVC ")
# # predictions = svm_detector.predict(x_test)
# # print(classification_report(label_test, predictions))
# print(grid_svm.score(x_test, label_test))

# # digits = datasets.load_digits()
# # y = digits.target
# # s = np.shape(y)
# # print(str(y[5:10]))
# # X, Y = make_multilabel_classification(n_classes=5, n_labels = 1,
# #                                       allow_unlabeled=False,
# #                                       random_state=1)

# # print(str(Y[0:5,:]))

# # s = [np.zeros(10)[i]=1 for i in [1:10]]
# # print(s)