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
analyzed_data = quail.analyze(egg, analysis='accuracy', listgroup=['average']*16)

#plot by list
quail.plot(analyzed_data, title='Average Recall Accuracy')
