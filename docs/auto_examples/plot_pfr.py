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
egg = quail.load_example_data()

# analysis
analyzed_data = quail.analyze(egg, analysis='pfr', listgroup=['average']*16)

# plot
quail.plot(analyzed_data, title='Probability of First Recall')
