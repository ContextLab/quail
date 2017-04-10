# -*- coding: utf-8 -*-
"""
=============================
Plot serial position curve
=============================

This example plots the probability of recall success as a function of serial
position during stimulus encoding

"""

# Code source: Andrew Heusser
# License: MIT

# import
import quail

# presented words
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]

# recalled words
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]

# create egg object
egg = quail.Egg(pres=presented,rec=recalled)

#analysis
analyzed_data = quail.analyze(egg, analysis='spc')

#plot
quail.plot(analyzed_data)
