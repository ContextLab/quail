# -*- coding: utf-8 -*-

from quail.analysis.analysis import analyze
from quail.load import load_example_data
from quail.egg import Egg
import numpy as np
import pytest
import pandas as pd

presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
egg = Egg(pres=presented,rec=recalled)

def test_analysis_acc():
    print(analyze(egg, analysis='accuracy'))
    print([np.array([1.]),np.array([.75])])
    assert np.array_equal(analyze(egg, analysis='accuracy').data.values,[np.array([1.]),np.array([.75])])

def test_analysis_spc():
    assert np.array_equal(analyze(egg, analysis='spc').data.values,[np.array([ 1.,  1.,  1.,  1.]),np.array([ 1.,  1.,  0.,  1.])])

def test_analysis_spc_listgroup():
    assert np.array_equal(analyze(egg, listgroup=[1,1], listname='Frank', analysis='spc').data.values,np.array([[ 1. ,  1. ,  0.5,  1. ]]))

def test_analysis_pfr():
    assert np.array_equal(analyze(egg, analysis='pfr').data.values,[np.array([ 0.,  1.,  0.,  0.]), np.array([ 0.,  1.,  0.,  0.])])

def test_analysis_pfr_listgroup():
    assert np.array_equal(analyze(egg, listgroup=['one','one'], analysis='pfr').data.values,np.array([[ 0.,  1.,  0.,  0.]]))

def test_analysis_lag_crp():
    # example from kahana lab lag-crp tutorial
    presented=[[['1', '2', '3', '4', '5', '6', '7', '8']]]
    recalled=[[['8', '7', '1', '2', '3', '5', '6', '4']]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.allclose(analyze(egg, analysis='lagcrp').data.values,np.array([[0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.333333, 0.333333, np.nan, 0.75, 0.333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]), equal_nan=True)

# MULTI SUBJECT
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']],[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']],[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
multisubj_egg = Egg(pres=presented,rec=recalled)

def test_analysis_acc_multisubj():
    assert np.array_equal(analyze(multisubj_egg, analysis='accuracy').data.values,np.array([[ 1.],[ .75],[ 1.],[ .75]]))

def test_analysis_spc_multisubj():
    assert np.array_equal(analyze(multisubj_egg, analysis='spc').data.values,np.array([[ 1.,  1.,  1.,  1.],[ 1.,  1.,  0.,  1.],[ 1.,  1.,  1.,  1.],[ 1.,  1.,  0.,  1.]]))

def test_egg():
    list1 = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    list2 = [[[10, 20], [30, 40]], [[50, 60], [70, 80]]]
    egg = Egg(pres = list1, rec = list2)
    assert type(egg.pres) == pd.core.frame.DataFrame
    assert type(egg.rec) == pd.core.frame.DataFrame

def test_load_example_data():
    egg = load_example_data()
    assert isinstance(egg, Egg)
