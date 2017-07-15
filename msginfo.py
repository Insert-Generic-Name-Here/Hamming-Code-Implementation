from sage.all import *
import numpy as np
import ast
import hashlib

def buildJson(word):
    json_msg = '{"msg": ['
    for vct in word:
        json_msg += "\""+repr(vct)+"\"" + ', '
    json_msg = json_msg[:-2] + ']}'
    return json_msg

def json2vct_arr(vct_str):
    return [vector(ast.literal_eval(vct)) for vct in vct_str]

def concatvct(arr):
    vct = arr[0]
    for tmp in arr[1::]:
        vct = vector(np.concatenate([vct, tmp]))
    return vct    

def entropy(labels): # labels = 0 / 1 vector
    n_labels = len(labels)
    #print n_labels
    if n_labels <= 1:
        return 0
    counts = np.bincount(labels)
    #print counts
    probs  = counts[np.nonzero(counts)] / float(n_labels)
    #print probs
    n_classes = len(probs)
    #print n_classes
    if n_classes <= 1:
        return 0
    return - np.sum(probs * np.log(probs)) / np.log(n_classes)

def sha256checksum(blst):
    return hashlib.sha256(blst).hexdigest()