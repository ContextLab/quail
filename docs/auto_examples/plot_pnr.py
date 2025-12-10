# -*- coding: utf-8 -*-
"""
=============================
Plot probability of nth recall
=============================

This example plots the probability of an item being recalled nth given its
list position.

"""

# Code source: Contextual Dynamics Laboratory
# License: MIT

# import
import quail

#load data
egg = quail.load('example')

# analyze and plot
fegg = egg.analyze('pnr', listgroup=['average']*8,
                              position=5)

fegg.plot(title='Probability of Recall')
