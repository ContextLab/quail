# -*- coding: utf-8 -*-
"""
=============================
Create an egg
=============================

An egg is made up of two primary pieces of data: `pres`, which are the
words/stimuli that were presented to a subject and `rec`, which are the
words/stimuli that were recalled by the subject.

"""

# Code source: Andrew Heusser
# License: MIT

import quail


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
                'category' : 'lambda a, b: int(a!=b)',
                'size' : 'lambda a, b: int(a!=b)',
                'starting letter' : 'lambda a, b: int(a!=b)',
                'length' : 'lambda a, b: np.linalg.norm(np.subtract(a,b))'
}
egg = quail.Egg(pres=[next_presented], rec=[next_recalled], features=[next_features], dist_funcs=dist_funcs)

egg.analyze('lagcrp').plot()
