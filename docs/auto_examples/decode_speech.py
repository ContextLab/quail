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

# decode speech
recall_data = quail.decode_speech('/Users/andyheusser/Documents/github/quail/data/sample.wav', save=True)

# print results
print(recall_data)
