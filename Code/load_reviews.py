# Load the data from the excel file ,and split it as 3 or 4 or 5 classes  

import pandas
import numpy as np

def loadXY(filename='reviews.xlsx'):
    train = pandas.read_excel(filename, header=None)
    y,X = train[1], train[2][:]
    X = X.tolist()
    y = y.tolist()
    X = X [1:]
    y =y[1:]
    y = np.array(y)
    return X,y

def load_dataset4Classes():
    X,y = loadXY()
    lowInd = np.where(y <=3)
    y[lowInd] = 11
    midInd1 = np.where(y <=5)
    y[midInd1] = 12
    midInd1 = np.where(y <=7)
    y[midInd1] = 13
    midInd1 = np.where(y <=10)
    y[midInd1] = 14
    return X,y

def load_dataset3Classes():
    X,y = loadXY()
    lowInd = np.where(y <=2)
    y[lowInd] = 11
    midInd1 = np.where(y <=4)
    y = np.delete(y,midInd1[0],None)
    X = np.delete(X,midInd1[0],None)
    midInd2 = np.where(y <=6)
    y[midInd2] = 12
    midInd3 = np.where(y <=8)
    y = np.delete(y,midInd3[0],None)
    X = np.delete(X,midInd3[0],None)
    midInd4 = np.where(y <=10)
    y[midInd4] = 13
    return X,y

def load_dataset2Classes():
    X,y = loadXY()
    lowInd = np.where(y <=4)
    y[lowInd] = 0
    highInd = np.where(y>= 7)
    y[highInd] = 1
    med = np.where(y >=5)
    y = np.delete(y,med[0],None)
    X = np.delete(X,med[0],None)
    return X,y

def load_dataset5Classes():
    X,y = loadXY()
    lowInd = np.where(y <=2)
    y[lowInd] = 11
    highInd = np.where(y<= 4)
    y[highInd] = 12
    med = np.where(y <=6)
    y[med] = 13
    med2 = np.where(y <=8)
    y[med2] = 14
    med22 = np.where(y <=10)
    y[med22] = 15
    return X,y