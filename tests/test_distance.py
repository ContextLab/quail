# -*- coding: utf-8 -*-

from quail.distance import *
import numpy as np
import pytest
from scipy.spatial.distance import cdist

def test_match():
    a = 'A'
    b = 'B'
    assert np.equal(match(a, b), 1)

def test_euclidean_list():
    a = [0, 1, 0]
    b = [0, 1, 0]
    assert np.equal(euclidean(a, b), 0)

def test_euclidean_array():
    a = np.array([0, 1, 0])
    b = np.array([0, 1, 0])
    assert np.equal(euclidean(a, b), 0)

def test_correlation_list():
    a = [0, 1, 0]
    b = [0, 1, 0]
    assert np.equal(correlation(a, b), 0)

def test_correlation_array():
    a = np.array([0, 1, 0])
    b = np.array([0, 1, 0])
    assert np.equal(correlation(a, b), 0)
