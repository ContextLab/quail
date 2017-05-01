# -*- coding: utf-8 -*-
"""
=============================
Plot free recall accuracy
=============================

This example plots free recall accuracy for a single subject.

"""

# Code source: Andrew Heusser
# License: MIT

#import
import quail

#load data
egg = quail.load_example_data()

#analysis
analyzed_data = quail.analyze(egg, analysis='accuracy', listgroup=['condition1']*8+['condition2']*8)

#plot by list
quail.plot(analyzed_data, plot_style='violin', title='Average Recall Accuracy')
