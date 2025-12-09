# -*- coding: utf-8 -*-
"""
=============================
Make egg out of recall matrix
=============================

This example shows how to make an egg out of a precomputed recall matrix so that
the analysis and plotting functions can be used.

"""

# Code source: Contextual Dynamics Laboratory
# License: MIT

# import
import quail

# create fake recall matrix
recmat = [[[5,4,3,0,1], [3,1,2,0]]]

# create egg
egg = quail.recmat2egg(recmat, list_length=6)
