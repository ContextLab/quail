from quail.egg import Egg
import numpy as np
import pytest

def test_acc():
    presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
    recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.allclose(egg.analyze('accuracy').data.values,[np.array([ 1.]),np.array([.75])])

def test_analysis_acc_multisubj():
    presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']],[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
    recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']],[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
    multisubj_egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(multisubj_egg.analyze('accuracy').data.values,np.array([[ 1.],[ .75],[1.],[.75]]))

def test_acc_best_euclidean():
    presented = [[[{'item' : i, 'feature1' : i*10} for i in range(1, 5)] for i in range(2)]]
    recalled=[[[{'item' : i, 'feature1' : i*10} for i in [2, 1, 4, 3]],[{'item' : i, 'feature1' : i*10} for i in [2, 4, 1]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('accuracy', match='best', distance='euclidean', features=['feature1']).data.values,[np.array([1.]),np.array([.75])])

def test_acc_best_euclidean_3d():
    presented = [[[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in range(1, 5)] for i in range(2)]]
    recalled=[[[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in [2, 1, 4, 3]],[{'item' : i, 'feature1' : [i*10, 0, 0]} for i in [2, 4, 1]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('accuracy', match='best', distance='euclidean', features='feature1').data.values,[np.array([1.]),np.array([.75])])

def test_acc_best_euclidean_3d_2features():
    presented = [[[{'item' : i, 'feature1' : [i*10, 0, 0], 'feature2' : 0} for i in range(1, 5)] for i in range(2)]]
    recalled=[[[{'item' : i, 'feature1' : [i*10, 0, 0], 'feature2': 0} for i in [2, 1, 4, 3]],[{'item' : i, 'feature1' : [i*10, 0, 0], 'feature2':0} for i in [2, 4, 1]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('accuracy', match='best', distance='euclidean', features=['feature1', 'feature2']).data.values,[np.array([1.]),np.array([.75])])

def test_acc_best_euclidean_3d_exception_item_specified():
    presented=[[[[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]],
                [[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0]]]]
    recalled=[[[[20, 0, 0], [10, 0, 0], [40, 0, 0], [30, 0, 0]],
               [[20, 0, 0], [40, 0, 0], [10, 0, 0]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('accuracy', match='best', distance='euclidean', features='item').data.values,[np.array([1.]),np.array([.75])])

def test_acc_best_correlation_3d():
    presented=[[[[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]],
                [[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]]]]
    recalled=[[[[20, 0, 0], [10, 0, 10], [40, 0, -20], [30, 0, -10]],
               [[20, 0, 0], [40, 0, -20], [10, 0, 10]]]]
    egg = Egg(pres=presented,rec=recalled)
    assert np.array_equal(egg.analyze('accuracy', match='best', distance='correlation', features='item').data.values,[np.array([1.]),np.array([.75])])

def test_acc_smooth_correlation_3d():
    presented=[[[[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]],
                [[10, 0, 10], [20, 0, 0], [30, 0, -10], [40, 0, -20]]]]
    recalled=[[[[20, 0, 0], [10, 0, 10], [40, 0, -20], [30, 0, -10]],
               [[20, 0, 0], [40, 0, -20], [10, 0, 10]]]]
    egg = Egg(pres=presented,rec=recalled)
    egg.analyze('spc', match='smooth', distance='correlation', features='item').data.values
