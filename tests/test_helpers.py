import pytest
import quail
import pandas as pd
import numpy as np
from quail.helpers import list2pd, recmat2egg, stack_eggs, crack_egg, shuffle_egg, r2z, z2r

def test_list2pd_basic():
    # Input should be List[Subject]. Subject = List[List].
    # 2 Subjs, 1 list each, 2 items each.
    data = [[['a', 'b']], [['c', 'd']]]
    df = list2pd(data)
    assert isinstance(df, pd.DataFrame)
    # 2 rows (1 per subj/list), 2 cols (items)
    assert df.shape == (2, 2)
    assert df.index.names == ['Subject', 'List']

def test_list2pd_empty():
    df = list2pd([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty
    
    df = list2pd([[]])
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_recmat2egg():
    recmat = [[[0, 1, 2], [3, 4, 5]]] # 1 subj, 2 lists
    egg = recmat2egg(recmat, list_length=10)
    assert isinstance(egg, quail.Egg)
    assert egg.n_subjects == 1
    assert egg.n_lists == 2
    # Pres items should be dicts
    assert egg.pres.iloc[0, 0]['item'] == '0'

def test_stack_eggs():
    pres = [[['a', 'b']]]
    rec = [[['a', 'b']]]
    # Meta values should be lists to support concatenation if logic naive
    egg1 = quail.Egg(pres=pres, rec=rec, meta={'foo': [1]})
    egg2 = quail.Egg(pres=pres, rec=rec, meta={'bar': [2]})
    
    stacked = stack_eggs([egg1, egg2])
    assert stacked.n_subjects == 2
    assert stacked.meta['foo'] == [1] 
    
    # Test meta='concatenate'
    egg3 = quail.Egg(pres=pres, rec=rec, meta={'foo': [3]})
    stacked_cat = stack_eggs([egg1, egg3], meta='concatenate')
    # Concatenation extends the list
    assert stacked_cat.meta['foo'] == [1, 3]

def test_crack_egg():
    pres = [[['a', 'b'], ['c', 'd']], [['e', 'f'], ['g', 'h']]] # 2 subjs, 2 lists
    rec = pres
    egg = quail.Egg(pres=pres, rec=rec)
    
    # Crack subject 0
    cracked = crack_egg(egg, subjects=[0])
    assert cracked.n_subjects == 1
    assert cracked.n_lists == 2
    
    # Crack list 0
    cracked = crack_egg(egg, lists=[0])
    assert cracked.n_subjects == 2
    assert cracked.n_lists == 1

def test_shuffle_egg():
    pres = [[['a', 'b', 'c']]]
    rec = [[['a', 'b', 'c']]]
    egg = quail.Egg(pres=pres, rec=rec)
    
    shuffled = shuffle_egg(egg)
    # Check shape
    assert shuffled.pres.shape == egg.pres.shape
    assert shuffled.rec.shape == egg.rec.shape
    # Check items are same set
    shuffled_items = [x['item'] for x in shuffled.rec.iloc[0].values]
    original_items = [x['item'] for x in egg.rec.iloc[0].values]
    assert set(shuffled_items) == set(original_items)

def test_fisher_z():
    r = 0.5
    z = r2z(r)
    r_back = z2r(z)
    assert np.isclose(r, r_back)
