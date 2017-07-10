import numpy as np
import hashlib

def entropy(labels): # labels = 0 / 1 vector
    n_labels = len(labels)

    if n_labels <= 1:
        return 0

    counts = np.bincount(labels)
    probs = counts[np.nonzero(counts)] / n_labels
    n_classes = len(probs)

    if n_classes <= 1:
        return 0
    return - np.sum(probs * np.log(probs)) / np.log(n_classes

def sha256checksum(blst):
    return hashlib.sha256(blst)