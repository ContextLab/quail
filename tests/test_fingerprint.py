from quail.egg import Egg
import numpy as np
import pytest

# generate some fake data
presented = ['CAT', 'DOG', 'SHOE', 'HORSE']
recalled = ['HORSE', 'DOG', 'CAT']

features = {'CAT' : {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'C',
                    'length' : 3
                 },
            'DOG' : {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'D',
                    'length' : 3
                 },
            'SHOE' : {
                    'category' : 'object',
                    'size' : 'smaller',
                    'starting letter' : 'S',
                    'length' : 4
                 },
            'HORSE' :  {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'H',
                    'length' : 5
                 }}

presented = list(map(lambda x: {'item' : x}, presented))
for p in presented:
    p.update(**features[p['item']])

recalled = list(map(lambda x: {'item' : x}, recalled))
for r in recalled:
    r.update(**features[r['item']])

egg = Egg(pres=[[presented]],rec=[[recalled]])

def test_fingerprint():
    assert np.allclose(egg.analyze('fingerprint', features=['category']).data.values[0], np.array([0.79166667]))

def test_fingerprint_permute_runs():
    assert egg.analyze('fingerprint', permute=True, n_perms=3)
