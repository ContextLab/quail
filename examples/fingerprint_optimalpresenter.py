# -*- coding: utf-8 -*-
import numpy as np
import quail
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

egg = quail.Egg(pres=[next_presented], rec=[next_recalled], features=[next_features],
                dist_funcs=dist_funcs)

# initialize fingerprint
fingerprint = Fingerprint(init=egg)

# initialize presenter
params = {
    'fingerprint' : fingerprint
}
presenter = OptimalPresenter(params=params, strategy='stabilize')

# update the fingerprint
fingerprint.update(egg)

# reorder next list
resorted_egg = presenter.order(egg, method='permute', nperms=100)

# print(resorted_egg.pres)
