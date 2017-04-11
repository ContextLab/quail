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

# presented words
presented_words = [['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]

# recalled words
recalled_words = [['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]

# create egg
egg = quail.Egg(pres=presented_words, rec=recalled_words)
