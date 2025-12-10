# -*- coding: utf-8 -*-
"""
=============================
Plot serial position curve
=============================

This example plots the probability of recall success as a function of serial
position during stimulus encoding.

"""

# Code source: Contextual Dynamics Laboratory
# License: MIT

# import
import quail

#load data
egg = quail.load('example')

# analyze and plot
fegg = egg.analyze('spc', listgroup=['average']*8)

fegg.plot(title='Serial Position Curve')
