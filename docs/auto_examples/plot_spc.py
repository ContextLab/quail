# -*- coding: utf-8 -*-
"""
=============================
Plot serial position curve
=============================

This example plots the probability of recall success as a function of serial
position during stimulus encoding.

"""

# Code source: Andrew Heusser
# License: MIT

# import
import quail

#load data
egg = quail.load_example_data()

#analysis
analyzed_data = quail.analyze(egg, analysis='spc', listgroup=['average']*8)

#plot
quail.plot(analyzed_data, title='Serial Position Curve')
