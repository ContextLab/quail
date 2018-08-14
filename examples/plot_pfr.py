# -*- coding: utf-8 -*-
"""
=============================
Plot probability of first recall
=============================

This example plots the probability of an item being recalled first given its
list position.

"""

# Code source: Andrew Heusser
# License: MIT

# import
import quail

#load data
egg = quail.load('example')

# analyze and plot
fegg = egg.analyze('pfr', listgroup=['average']*8)

fegg.plot(title='Probability of First Recall')
