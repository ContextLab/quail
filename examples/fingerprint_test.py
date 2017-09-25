# -*- coding: utf-8 -*-
import numpy as np
from quail import Fingerprint, OptimalPresenter

# generate some fake data
next_presented = ['CAT', 'DOG', 'SHOE', 'HORSE']
next_recalled = ['HORSE', 'DOG', 'CAT']
next_features = [{
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'C',
                    'length' : 3
                 },
                 {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'D',
                    'length' : 3
                 },
                 {
                    'category' : 'object',
                    'size' : 'smaller',
                    'starting letter' : 'S',
                    'length' : 4
                 },
                 {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'H',
                    'length' : 5
                 }
]
dist_funcs = {
                'category' : lambda a, b: int(a!=b),
                'size' : lambda a, b: int(a!=b),
                'starting letter' : lambda a, b: int(a!=b),
                'length' : lambda a, b: np.linalg.norm(np.subtract(a,b))
}

# initialize fingerprint
fingerprint = Fingerprint(features=dist_funcs.keys(), dist_funcs=dist_funcs)

# initialize presenter
params = {
    'fingerprint' : fingerprint
}
presenter = OptimalPresenter(params=params)

# update the fingerprint
fingerprint.update(next_presented, next_recalled, next_features)

# reorder next list
next_order = presenter.order(next_presented, )
