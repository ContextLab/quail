# -*- coding: utf-8 -*-

from quail.egg import Egg, FriedEgg
import pytest
import pandas as pd
import six
import matplotlib.pyplot as plt

presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
fried_egg = Egg(pres=presented,rec=recalled).analyze('accuracy')

def test_fried_egg_data_is_df():
    assert isinstance(fried_egg.data, pd.DataFrame)

def test_fried_egg_analysis():
    assert isinstance(fried_egg.analysis, six.string_types)
    assert fried_egg.analysis=='accuracy'

def test_fried_egg_listlength():
    assert fried_egg.list_length==4

def test_fried_egg_n_lists():
    assert fried_egg.n_lists==2

def test_fried_egg_n_subjects():
    assert fried_egg.n_subjects==1

def test_fried_egg_position():
    assert fried_egg.position==0

def test_fried_egg_plot():
    isinstance(fried_egg.plot(show=False), plt.Figure)
