# -*- coding: utf-8 -*-
"""
=============================
Create an egg
=============================

An egg is made up of two primary pieces of data: `pres`, which are the
words/stimuli that were presented to a subject and `rec`, which are the
words/stimuli that were recalled by the subject.

"""

# Code source: Andrew Heusser
# License: MIT

import quail
import numpy as np

# presented words
presented_words = [[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']],[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]

# recalled words
recalled_words = [[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']],[['bat', 'cat', 'goat'],['animal', 'horse']]]

# create egg
egg = quail.Egg(pres=presented_words, rec=recalled_words)

#analysis
analyzed_data = quail.analyze(egg, analysis='accuracy')

#plot by list
quail.plot(analyzed_data, plot_style='violin', title='Average Recall Accuracy')
