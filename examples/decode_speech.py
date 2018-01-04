# -*- coding: utf-8 -*-
"""
=============================
Decode speech
=============================

This example plots free recall accuracy for a single subject.

"""

# Code source: Andrew Heusser
# License: MIT

#import
import quail

# decode speech
recall_data = quail.decode_speech('../data/sample.wav', save=True, speech_context=['DONKEY', 'PETUNIA'])

# print results
print(recall_data)
