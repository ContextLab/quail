# -*- coding: utf-8 -*-
"""
=============================
Plot memory fingerprint
=============================

This example plots a fingerprint.  Briefly, a fingerprint
can be described as a summary of how a subject organizes information with
respect to the multiple features of the stimuli.  In addition to presentation
and recall data, a features object is passed to the Egg class.  It is comprised
of a dictionary for each presented stimulus that contains feature dimensions and
values for each stimulus.

"""

# Code source: Andrew Heusser
# License: MIT

#import
import quail

#load data
egg = quail.load_example_data()

# analysis
analyzed_data = quail.analyze(egg, analysis='fingerprint_temporal', listgroup=['average']*16)

# plot
quail.plot(analyzed_data, title='Memory Fingerprint')
