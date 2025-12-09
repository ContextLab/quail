# -*- coding: utf-8 -*-
"""
=============================
Plot free recall accuracy
=============================

This example plots free recall accuracy for a single subject.

"""

# Code source: Contextual Dynamics Laboratory
# License: MIT

#import
import quail

#load data
egg = quail.load('example')

#analysis
fegg = egg.analyze('accuracy', listgroup=['condition1']*4+['condition2']*4)

#plot by list
fegg.plot(plot_style='violin', title='Average Recall Accuracy')
