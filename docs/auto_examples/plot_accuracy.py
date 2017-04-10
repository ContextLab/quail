# -*- coding: utf-8 -*-
"""
=============================
Plot free recall accuracy
=============================

This example plots free recall accuracy for a single subject.  Without any flags,
each list will be plotted separately. To plot the average, set the plot_type
kwarg to subject.  Finally, to change the style, you can pass the plot_style
kwarg, setting it to bar, violin or swarm.

"""

# Code source: Andrew Heusser
# License: MIT

#import
import quail

# presented words
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]

# recalled words
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]

# create the egg data object
egg = quail.Egg(pres=presented,rec=recalled)

#analysis
analyzed_data = quail.analyze(egg, analysis='accuracy')

#plot by list
quail.plot(analyzed_data)

#plot averaged over lists
quail.plot(analyzed_data, plot_type='subject')
