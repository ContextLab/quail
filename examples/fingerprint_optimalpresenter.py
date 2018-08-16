# -*- coding: utf-8 -*-
"""
=============================
Optimal presenter
=============================

An example of how to reorder stimuli with the optimal presenter class

"""

# Code source: Andrew Heusser
# License: MIT

import numpy as np
import quail
from quail import Fingerprint, OptimalPresenter

# generate some fake data
next_presented = [{
                    'item' : 'CAT',
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'C',
                    'length' : 3
                 },
                 {
                    'item' : 'DOG',
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'D',
                    'length' : 3
                 },
                 {
                    'item' : 'SHOE',
                    'category' : 'object',
                    'size' : 'smaller',
                    'starting letter' : 'S',
                    'length' : 4
                 },
                 {
                    'item' : 'BAT',
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'B',
                    'length' : 3
                 }]

next_recalled = [{
                    'item' : 'DOG',
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'D',
                    'length' : 3
                 },
                 {
                    'item' : 'CAT',
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'C',
                    'length' : 3
                 },
                 {
                    'item' : 'BAT',
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'B',
                    'length' : 3
                 },
                 {
                    'item' : 'SHOE',
                    'category' : 'object',
                    'size' : 'smaller',
                    'starting letter' : 'S',
                    'length' : 4
                 }
]

egg = quail.Egg(pres=[next_presented], rec=[next_recalled])

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
