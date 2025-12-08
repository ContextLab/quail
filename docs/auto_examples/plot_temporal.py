# -*- coding: utf-8 -*-
"""
=============================
Plot temporal clustering
=============================

This example plots temporal clustering, the extent to which subject tend to
recall neighboring items sequentially.

"""

# Code source: Andrew Heusser
# License: MIT

# import
import quail

#load data
egg = quail.load('example')

#analyze and plot
fegg = egg.analyze('temporal', listgroup=['early']*4+['late']*4)

fegg.plot(title='Temporal Clustering')
