# -*- coding: utf-8 -*-
"""
=============================
Plot memory fingerprint
=============================

This example plots a fingerprint for a single subject.  Briefly, a fingerprint
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

# presented words
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'donkey', 'zebra', 'horse']]]

# recalled words
recalled=[[['bat', 'cat', 'goat', 'hat'],['donkey', 'horse', 'zoo']]]

# presentation features
features = [
    [
        [
            {
                'category' : 'animal',
                'word_length' : 3,
                'starting_letter' : 'c'
            },
            {
                'category' : 'object',
                'word_length' : 3,
                'starting_letter' : 'b'
            },
            {
                'category' : 'object',
                'word_length' : 3,
                'starting_letter' : 'h'
            },
            {
                'category' : 'animal',
                'word_length' : 4,
                'starting_letter' : 'g'
            },
        ],
        [
            {
                'category' : 'place',
                'word_length' : 3,
                'starting_letter' : 'z'
            },
            {
                'category' : 'animal',
                'word_length' : 6,
                'starting_letter' : 'd'
            },
            {
                'category' : 'animal',
                'word_length' : 5,
                'starting_letter' : 'z'
            },
            {
                'category' : 'animal',
                'word_length' : 5,
                'starting_letter' : 'h'
            },
        ],
    ]
]

# create egg object
egg = quail.Egg(pres=presented, rec=recalled, features=features)

# analysis
analyzed_data = quail.analyze(egg, analysis='fingerprint')

# plot
quail.plot(analyzed_data)
