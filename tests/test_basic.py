# -*- coding: utf-8 -*-

from pyrec.analysis import recall_matrix
from pyrec.analysis import spc
from pyrec.analysis import pfr
from pyrec.analysis import plr
from pyrec.analysis import lag_crp

from pyrec.pyro import Pyro
import numpy as np
import pytest
import pandas as pd

presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
pyro = Pyro(pres=presented,rec=recalled)

def test_analysis_spc():
	assert np.array_equal(spc(pyro).values,[np.array([ 1.,  1.,  1.,  1.]),np.array([ 1.,  1.,  0.,  1.])])

def test_analysis_spc_listgroup():
	assert np.array_equal(spc(pyro, listgroup=[1,1], listname='Frank').values,np.array([[ 1. ,  1. ,  0.5,  1. ]]))

def test_analysis_pfr():
	assert np.array_equal(pfr(pyro).values,[np.array([ 0.,  1.,  0.,  0.]), np.array([ 0.,  1.,  0.,  0.])])

def test_analysis_pfr_listgroup():
	assert np.array_equal(pfr(pyro, listgroup=['one','one']).values,np.array([[ 0.,  1.,  0.,  0.]]))

def test_analysis_plr():
	assert np.array_equal(plr(pyro).values,[np.array([ 0.,  0.,  1.,  0.]), np.array([ 1.,  0.,  0.,  0.])])

def test_analysis_plr_listgroup():
	assert np.array_equal(plr(pyro, listgroup=[1,1]).values,np.array([[ 0.5,  0.,  0.5,  0.]]))

# def test_analysis_lag_crp():
# 	assert np.array_equal(lag_crp(pyro).values,np.array([[0.0, 0.0, 1.0, 0.0, 0.0, 1.0],[1.0, 0.0, 0.0, 0.0, 0.5, 0.0]]))

# MULTI SUBJECT
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']],[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']],[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
multisubj_pyro = Pyro(pres=presented,rec=recalled)

def test_analysis_spc_multisubj():
	assert np.array_equal(spc(multisubj_pyro).values,np.array([[ 1.,  1.,  1.,  1.],[ 1.,  1.,  0.,  1.],[ 1.,  1.,  1.,  1.],[ 1.,  1.,  0.,  1.]]))

def test_analysis_spc_listgroup_subjgroup():
	assert np.array_equal(spc(multisubj_pyro, subjgroup=[1,1], listgroup=[1,1]).values,[np.array([ 1. ,  1. ,  0.5,  1. ])])

def test_pyro():
	list1 = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
 	list2 = [[[10, 20], [30, 40]], [[50, 60], [70, 80]]]

 	pyro = Pyro(pres = list1, rec = list2)
 	assert type(pyro.pres) == pd.core.frame.DataFrame
 	assert type(pyro.rec) == pd.core.frame.DataFrame
