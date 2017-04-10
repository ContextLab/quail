# -*- coding: utf-8 -*-
"""
=============================
Plot Lag-CRP for a single subject
=============================

This example plots a Lag-CRP for a subject as described in Kahana et al (1996).
Given the recall of a stimulus in position n, this plot shows the probability of
recalling stimuli in neighboring stimulus positions (n+/-5).

"""

# Code source: Andrew Heusser
# License: MIT

#import
import quail

# presented words
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]

# recalled words
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]

#create egg object
egg = quail.Egg(pres=presented,rec=recalled)

#analysis
analyzed_data = quail.analyze(egg, analysis='lagcrp', listgroup=['average']*2)

#plot
quail.plot(analyzed_data)
