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
egg = quail.load_example_data()

#crack egg
cracked_egg = quail.crack_egg(egg, subjects=range(5), lists=range(4))

cracked_egg.info()
