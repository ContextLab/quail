# -*- coding: utf-8 -*-
import numpy as np
import quail
from quail import Fingerprint, OptimalPresenter

# generate some fake data
next_presented = ['CAT', 'DOG', 'SHOE', 'BAT']
next_recalled = ['DOG', 'CAT', 'BAT', 'SHOE']

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
                    'starting letter' : 'B',
                    'length' : 3
                 }]

egg = quail.Egg(pres=[next_presented], rec=[next_recalled], features=[next_features])

# initialize fingerprint
fingerprint = Fingerprint(init=egg)

# initialize presenter
params = {
    'fingerprint' : fingerprint}
presenter = OptimalPresenter(params=params, strategy='stabilize')

# update the fingerprint
fingerprint.update(egg)

# reorder next list
reordered_egg = presenter.order(egg, method='permute', nperms=100)
