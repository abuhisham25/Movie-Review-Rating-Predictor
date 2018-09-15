import pandas
import numpy as np
def load_dataset(filename1='revs_4Class', filename2='label_4Class'):
    # train = pandas.read_excel(filename, header=None)
    # y,X = train[1], train[2][:]
    X = open(filename1, "r").read().split("\n")
    y = open(filename2, "r").read().split("\n")
    # X = X.tolist()
    # y = y.tolist()
    # X = X [1:]
    # y =y[1:]
    return X,y
load_dataset()