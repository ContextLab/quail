#!/usr/bin/env python
import numpy as np
from scipy.spatial.distance import cdist

def match(a, b):
    "Returns 0 if match and 1 otherwise"
    return int(not np.array_equal(a, b))

def correlation(a, b):
    "Returns correlation distance between a and b"
    if isinstance(a, list):
        a = np.array(a)
    if isinstance(b, list):
        b = np.array(b)
    a = a.reshape(1, -1)
    b = b.reshape(1, -1)
    return cdist(a, b, 'correlation')

def euclidean(a, b):
    "Returns euclidean distance between a and b"
    return np.linalg.norm(np.subtract(a, b))

dist_funcs = {
    'match' : match,
    'correlation' : correlation,
    'euclidean' : euclidean
}
