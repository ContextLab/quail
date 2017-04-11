# -*- coding: utf-8 -*-
"""
=============================
Load in some data
=============================

The sample data is a list of 2D arrays, where each array is fMRI brain activity
from one subject.  The rows are timepoints and the columns are neural
'features'.  First, the matrices are hyperaligned using hyp.tools.align.
"""

# Code source: Andrew Heusser
# License: MIT

import quail

dbpath = '/Users/andyheusser/Documents/github/FRFR-analyses/data/encoding/participants-test-room1.db'
recpath = '/Users/andyheusser/Documents/github/FRFR-analyses/data/recall/room1/'
remove_subs = ['debugCWO54U:debugQ59MF8', 'debugE1CAO3:debugONZ2R5', 'debugXG82XV:debug7XPXQA']
wordpool = '/Users/andyheusser/Documents/github/FRFR-analyses/stimuli/cut_wordpool.csv'

# create an egg with all data
egg_all = quail.load(dbpath=dbpath, recpath=recpath, remove_subs=remove_subs,
                  wordpool=wordpool)

# create a list of eggs, where each egg is a different experiment
groupby = {'exp_version': [['0.0','1.0','1.1'], '2.1', '3.2', '4.1', '5.1']}
eggs = quail.load(dbpath=dbpath, recpath=recpath, remove_subs=remove_subs,
                  wordpool=wordpool, groupby=groupby)
