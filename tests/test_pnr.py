from quail.egg import Egg
import numpy as np
import pytest

def test_analysis_pfr():
    presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
    recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr').data.values,[np.array([ 0.,  1.,  0.,  0.]), np.array([ 0.,  1.,  0.,  0.])])

def test_analysis_pnr():
    presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
    recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
    egg = Egg(pres=presented, rec=recalled)
    assert np.array_equal(egg.analyze('pnr', position=1).data.values, [np.array([ 1.,  0.,  0.,  0.]), np.array([ 0.,  0.,  0.,  1.])])

def test_pfr_best_euclidean():
    presented=[[[10, 20, 30, 40],[10, 20, 30, 40]]]
    recalled=[[[20, 10, 40, 30],[20, 40, 10]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr', match='best', distance='euclidean').data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])

def test_pfr_best_euclidean_3d():
    presented=[[[[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]],
                [[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]]]]
    recalled=[[[[20, 0, 0], [10, 0, 0], [40, 0, 0], [30, 0, 0]],
               [[20, 0, 0], [40, 0, 0], [10, 0, 0]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr', match='best', distance='euclidean').data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])
