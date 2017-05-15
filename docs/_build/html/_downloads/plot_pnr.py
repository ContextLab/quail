# -*- coding: utf-8 -*-
"""
=============================
Plot probability of nth recall
=============================

This example plots the probability of an item being recalled nth given its
list position.

"""

# Code source: Andrew Heusser
# License: MIT

# import
import quail

#load data
egg = quail.load_example_data()

# analysis
analyzed_data = quail.analyze(egg, analysis='pnr', listgroup=['average']*8, n=5)

# plot
quail.plot(analyzed_data, title='Probability of Recall')
