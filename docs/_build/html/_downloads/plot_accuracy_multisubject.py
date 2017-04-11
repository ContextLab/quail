# -*- coding: utf-8 -*-
"""
=============================
Plot free recall accuracy for a group of subjects
=============================

In this example, we plot the average recall accuracy for two subject's data. Using
the listgroup kwarg, we can average over the lists within each subject, and then
plot the result.

"""

# Code source: Andrew Heusser
# License: MIT

#import
import quail


# presented words
sub1_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
sub2_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]

# recalled words
sub1_recalled=[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]
sub2_recalled=[['cat', 'goat', 'bat', 'hat'],['horse', 'zebra', 'zoo', 'animal']]

# combine subject data
presented = [sub1_presented, sub2_presented]
recalled = [sub1_recalled, sub2_recalled]

# create Egg
egg = quail.Egg(pres=presented,rec=recalled)

#analysis
analyzed_data = quail.analyze(egg, analysis='accuracy', listgroup=['average']*2)

#plot
quail.plot(analyzed_data, title='Free Recall Accuracy', listname='')
