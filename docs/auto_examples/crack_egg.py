# -*- coding: utf-8 -*-
"""
=============================
Crack Egg
=============================

This an example of how to crack an egg (take a slice of subjects/lists from it)

"""

# Code source: Andrew Heusser
# License: MIT

#import
import quail

#load data
egg = quail.load('example')

#crack egg
cracked_egg = egg.crack(subjects=[0], lists=[0])

cracked_egg.info()
