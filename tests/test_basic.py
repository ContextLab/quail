# -*- coding: utf-8 -*-

from pyrec.analysis import recall_matrix
from pyrec.analysis import serial_pos
from pyrec.analysis import pfr
from pyrec.analysis import plr
from pyrec.analysis import crp
from pyrec.pyro import Pyro
import numpy as np
import pytest
import pandas as pd

def test_analysis_recall_matrix():
	presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
	recalled=[['bat', 'bat', 'cat', 'popsicle'],['animal', 'horse', 'cat']]

	assert recall_matrix(presented, recalled)==[[2, 2, 1, np.nan],[2, 4, -1, np.nan]]

def test_analysis_serial_pos():
	recall_matrix=[[4, 3, 1, 0, 0],[4, 5, 0, 0, 0]]
	assert np.array_equal(serial_pos(recall_matrix),np.array([.5, 0, .5, 1, .5]))

def test_analysis_pfr():
	recall_matrix1 =[[4, 3, 1, 0, 0],[4, 5, 0, 0, 0]] 
	recall_matrix2 =[[1, 2, 3],[3, 2, 1]]

	assert np.array_equal(pfr(recall_matrix1),np.array([0, 0, 0, 1, 0]))
	assert np.array_equal(pfr(recall_matrix2),np.array([.5, 0, .5]))

def test_analysis_plr():
	recall_matrix1 =[[4, 3, 1, 0, 0],[4, 5, 0, 0, 0]] 
	recall_matrix2 =[[1, 2, 3],[3, 2, 1]]
	recall_matrix3 =[[1, 2, 3],[3, 2, 3]]

	assert np.array_equal(plr(recall_matrix1),np.array([.5, 0, 0, 0, .5]))
	assert np.array_equal(plr(recall_matrix2),np.array([.5, 0, .5]))
	assert np.array_equal(plr(recall_matrix3),np.array([0, 0, 1]))

def test_analysis_crp():
	myList=[[8, 7, 1, 2, 3, 5, 6, 4],[8, 7, 1, 2, 3, 5, 6, 4]]
	assert crp(myList)==[[0.0, 0.5, 0.0, 0.0, 0.0, 0.33333333333333331, 0.33333333333333331, 0.75, 0.33333333333333331, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.5, 0.0, 0.0, 0.0, 0.33333333333333331, 0.33333333333333331, 0.75, 0.33333333333333331, 0.0, 0.0, 0.0, 0.0, 0.0]]

def test_pyro():
	list1 = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
 	list2 = [[[10, 20], [30, 40]], [[50, 60], [70, 80]]]

 	pyro = Pyro(pres = list1, rec = list2)
 	assert type(pyro.pres) == pd.core.frame.DataFrame
 	assert type(pyro.rec) == pd.core.frame.DataFrame