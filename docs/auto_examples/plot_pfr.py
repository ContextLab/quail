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

# presented words
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]

# recalled words
recalled=[[['bat', 'cat', 'goat', 'hat'],['zebra', 'horse', 'zoo']]]

# create egg object
egg = quail.Egg(pres=presented,rec=recalled)

# analysis
analyzed_data = quail.analyze(egg, analysis='pfr')

# plot
quail.plot(analyzed_data)
