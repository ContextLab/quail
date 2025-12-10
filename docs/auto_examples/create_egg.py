# -*- coding: utf-8 -*-
"""
=============================
Create an egg
=============================

An egg is made up of two primary pieces of data: `pres`, which are the
words/stimuli that were presented to a subject and `rec`, which are the
words/stimuli that were recalled by the subject.

"""

# Code source: Contextual Dynamics Laboratory
# License: MIT

import quail


# generate some fake data
presented = [{
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
                    'item' : 'HORSE',
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'H',
                    'length' : 5
                 }
]

recalled = [{
                    'item' : 'HORSE',
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'H',
                    'length' : 5
                 },
                 {
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
                 }
]

# set some custom distance functions
dist_funcs = {
                'category' : 'lambda a, b: int(a!=b)',
                'size' : 'lambda a, b: int(a!=b)',
                'starting letter' : 'lambda a, b: int(a!=b)',
                'length' : 'lambda a, b: np.linalg.norm(np.subtract(a,b))'
}

egg = quail.Egg(pres=[presented], rec=[recalled], dist_funcs=dist_funcs)

fegg = egg.analyze('lagcrp')

fegg.plot()
