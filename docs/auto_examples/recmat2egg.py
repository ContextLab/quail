# -*- coding: utf-8 -*-
"""
=============================
recmat2egg
=============================

This example plots the probability of recall success as a function of serial
position during stimulus encoding

"""

# Code source: Andrew Heusser
# License: MIT

#import
import quail as quail

#create egg object using recmat2egg
recmat = [[[2, 3, 0, None], [2, 3, 1, 0]]]
egg = quail.helpers.recmat2egg(recmat)

#analysis
analyzed_data = quail.analyze(egg, listgroup=[1,1], analysis='spc')

#plot
quail.plot(analyzed_data)
