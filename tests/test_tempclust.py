# -*- coding: utf-8 -*-

from quail.analysis import analyze

from quail.egg import Egg
import numpy as np
import pytest
import pandas as pd

# test that temporal clustering is one if words recited forward
def test_analysis_tempclust_forwards():
    presented=[[['cat', 'bat', 'hat', 'goat']]]
    recalled=[[['cat', 'bat', 'hat', 'goat']]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(analyze(egg, analysis='tempclust')[0].values,[1])

# test that temporal clustering is one if words recited backwards
def test_analysis_tempclust_backwards():
    presented=[[['cat', 'bat', 'hat', 'goat']]]
    recalled=[[['goat', 'hat', 'bat', 'cat']]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(analyze(egg, analysis='tempclust')[0].values,[1])

# test that temporal clustering is one if words recited backwards
def test_analysis_tempclust_rand():
    presented=[[['cat', 'bat', 'hat', 'goat']]]
    for i in range(10):
        rec_perm = [[[str(i) for i in np.random.permutation(['goat', 'cat', 'bat', 'hat'])]]]
        egg = Egg(pres=presented,rec=rec_perm)
    assert False
