# -*- coding: utf-8 -*-
"""
=============================
Plot probability of nth recall matrix
=============================

This example plots the probability of an item being recalled nth given its nth list position

"""

# Code source: Paxton Fitzpatrick
# License: MIT

# import
import quail

#load data
egg = quail.load_example_data()

# analysis
analyzed_data = quail.analyze(egg, analysis='pnr_matrix', listgroup=['average']*8, n=5)

# plot
quail.plot(analyzed_data, title='Probability of Recall')
