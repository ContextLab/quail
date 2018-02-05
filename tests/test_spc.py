from quail.egg import Egg
import numpy as np
import pytest

def test_spc():
    presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
    recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('spc').data.values,[np.array([ 1.,  1.,  1.,  1.]),np.array([ 1.,  1.,  0.,  1.])])

def test_analysis_spc_multisubj():
    presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']],[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
    recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']],[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
    multisubj_egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(multisubj_egg.analyze('spc').data.values,np.array([[ 1.,  1.,  1.,  1.],[ 1.,  1.,  0.,  1.],[ 1.,  1.,  1.,  1.],[ 1.,  1.,  0.,  1.]]))

def test_spc_best_euclidean():
    presented=[[[10, 20, 30, 40],[10, 20, 30, 40]]]
    recalled=[[[20, 10, 40, 30],[20, 40, 10]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('spc', match='best', distance='euclidean').data.values,[np.array([1., 1., 1., 1.]),np.array([1., 1., 0., 1.])])

def test_acc_best_euclidean_3d():
    presented=[[[[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]],
                [[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]]]]
    recalled=[[[[20, 0, 0], [10, 0, 0], [40, 0, 0], [30, 0, 0]],
               [[20, 0, 0], [40, 0, 0], [10, 0, 0]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('spc', match='best', distance='euclidean').data.values,[np.array([1., 1., 1., 1.]),np.array([1., 1., 0., 1.])])

def test_acc_smooth_correlation_3d():
    presented=[[[[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]],
                [[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]]]]
    recalled=[[[[20, 0, 0], [10, 0, 10], [40, 0, -20], [30, 0, -10]],
               [[20, 0, 0], [40, 0, -20], [10, 0, 10]]]]
    egg = Egg(pres=presented,rec=recalled)
    egg.analyze('spc', match='smooth', distance='correlation').data.values
