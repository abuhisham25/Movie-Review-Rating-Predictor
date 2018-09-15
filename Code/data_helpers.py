import numpy as np
import re
from load_reviews import *

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets .
    """
    string = string.replace("<p>",'')
    string = string.replace("</p>",'')
    string = string.replace("\n",' ')
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(classNum):
    """
    Loads data from files, splits the data into words .
    Returns split sentences and labels.
    """
    if classNum == 2:
        x_text,y = load_dataset2Classes()
    elif classNum == 3:
        x_text,y = load_dataset3Classes()
    elif classNum == 4:
        x_text,y = load_dataset4Classes()
    elif classNum == 5:
        x_text,y = load_dataset5Classes()
    x_text = [clean_str(sent) for sent in x_text]
    return [x_text, y]
