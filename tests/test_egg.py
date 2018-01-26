# -*- coding: utf-8 -*-

from quail.analysis import analyze
from quail.egg import Egg, FriedEgg
import pytest
import pandas as pd
import six

presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
egg = Egg(pres=presented,rec=recalled)

def test_egg_works():
    assert isinstance(egg, Egg)

def test_pres_is_df():
    assert isinstance(egg.pres, pd.DataFrame)

def test_rec_is_df():
    assert isinstance(egg.rec, pd.DataFrame)

def test_pres_cells_are_dicts():
    assert isinstance(egg.pres.loc[0][0][0], dict)

def test_pres_cells_has_item():
    assert egg.pres.loc[0][0][0]['item']=='cat'

def test_pres_cells_has_item():
    assert egg.rec.loc[0][0][0]['item']=='bat'

def test_distfuncs_is_dict():
    assert isinstance(egg.dist_funcs, dict)

def test_egg_meta():
    assert isinstance(egg.meta, dict)

def test_egg_get_pres_items():
    assert isinstance(egg.get_pres_items(), pd.DataFrame)

def test_egg_get_pres_items_cat():
    assert egg.get_pres_items()[0][0][0]=='cat'

def test_egg_get_pres_features():
    assert isinstance(egg.get_pres_features(), pd.DataFrame)

def test_egg_get_rec_items():
    assert isinstance(egg.get_rec_items(), pd.DataFrame)

def test_egg_get_rec_items_cat():
    assert egg.get_rec_items()[0][0][0]=='bat'

def test_egg_get_rec_features():
    assert isinstance(egg.get_rec_features(), pd.DataFrame)

def test_egg_crack():
    assert isinstance(egg.crack(), Egg)

def test_egg_crack_n_lists():
    assert egg.crack(lists=[0]).n_lists==1

def test_egg_to_dict():
    assert isinstance(egg.to_dict(), dict)

def test_egg_analyze():
    assert isinstance(egg.analyze('accuracy'), FriedEgg)

def test_egg_analyze_error():
    with pytest.raises(ValueError):
        egg.analyze('acc')
