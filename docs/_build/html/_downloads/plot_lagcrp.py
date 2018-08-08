# -*- coding: utf-8 -*-
"""
=============================
Plot Lag-CRP
=============================

This example plots a Lag-CRP as described in Kahana et al (1996).
Given the recall of a stimulus in position n, this plot shows the probability of
recalling stimuli in neighboring stimulus positions (n+/-5).

"""

# Code source: Andrew Heusser
# License: MIT

# import
import quail

# load data
egg = quail.load('example')

# analyze and plot
egg.analyze('lagcrp', listgroup=['average']*8).plot(title='Lag-CRP')
