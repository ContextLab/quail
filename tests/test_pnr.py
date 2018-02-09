from quail.egg import Egg
import numpy as np
import pytest

def test_analysis_pfr():
    presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
    recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr').data.values,[np.array([ 0.,  1.,  0.,  0.]), np.array([ 0.,  1.,  0.,  0.])])

def test_analysis_pnr_pos1():
    presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
    recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
    egg = Egg(pres=presented, rec=recalled)
    assert np.array_equal(egg.analyze('pnr', position=1).data.values, [np.array([ 1.,  0.,  0.,  0.]), np.array([ 0.,  0.,  0.,  1.])])
#
def test_pfr_best_euclidean():
    presented = [[[{'item' : i, 'feature1' : i*10} for i in range(1, 5)] for i in range(2)]]
    recalled=[[[{'item' : i, 'feature1' : i*10} for i in [2, 1, 4, 3]],[{'item' : i, 'feature1' : i*10} for i in [2, 4, 1]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr', match='best', distance='euclidean').data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])
#
def test_pfr_best_euclidean_3d():
    presented = [[[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in range(1, 5)] for i in range(2)]]
    recalled=[[[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in [2, 1, 4, 3]],[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in [2, 4, 1]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr', match='best', distance='euclidean').data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])

def test_pfr_best_euclidean_3d_2features():
    presented = [[[{'item' : i, 'feature1' : [i*10, 0, 0], 'feature2' : 0} for i in range(1, 5)] for i in range(2)]]
    recalled=[[[{'item' : i, 'feature1' : [i*10, 0, 0], 'feature2': 0} for i in [2, 1, 4, 3]],[{'item' : i, 'feature1' : [i*10, 0, 0], 'feature2':0} for i in [2, 4, 1]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr', match='best', distance='euclidean', features=['feature1', 'feature2']).data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])

def test_acc_best_euclidean_3d_features_not_set():
    presented = [[[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in range(1, 5)] for i in range(2)]]
    recalled=[[[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in [2, 1, 4, 3]],[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in [2, 4, 1]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr', match='best', distance='euclidean').data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])

def test_pfr_best_euclidean_3d_exception_no_features():
    presented=[[[[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]],
                [[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]]]]
    recalled=[[[[20, 0, 0], [10, 0, 0], [40, 0, 0], [30, 0, 0]],
               [[20, 0, 0], [40, 0, 0], [10, 0, 0]]]]
    egg = Egg(pres=presented,rec=recalled)
    with pytest.raises(Exception):
        assert np.array_equal(egg.analyze('pfr', match='best', distance='euclidean').data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])

def test_pfr_best_euclidean_3d_exception_item_specified():
    presented=[[[[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]],
                [[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]]]]
    recalled=[[[[20, 0, 0], [10, 0, 0], [40, 0, 0], [30, 0, 0]],
               [[20, 0, 0], [40, 0, 0], [10, 0, 0]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr', match='best', distance='euclidean', features='item').data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])

def test_pfr_best_correlation_3d():
    presented=[[[[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]],
                [[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]]]]
    recalled=[[[[20, 0, 0], [10, 0, 10], [40, 0, -20], [30, 0, -10]],
               [[20, 0, 0], [40, 0, -20], [10, 0, 10]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('pfr', match='best', distance='correlation', features='item').data.values,[np.array([0., 1., 0., 0.]),np.array([0., 1., 0., 0.])])

def test_pfr_smooth_correlation_3d():
    presented=[[[[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]],
                [[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]]]]
    recalled=[[[[20, 0, 0], [10, 0, 10], [40, 0, -20], [30, 0, -10]],
               [[20, 0, 0], [40, 0, -20], [10, 0, 10]]]]
    egg = Egg(pres=presented,rec=recalled)
    egg.analyze('pfr', match='smooth', distance='correlation', features='item').data.values
