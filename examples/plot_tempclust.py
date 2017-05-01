# -*- coding: utf-8 -*-
"""
=============================
Plot temporal clustering
=============================

This example plots temporal clustering, the extent to which subject tend to
recall neighboring items sequentially

"""

# Code source: Andrew Heusser
# License: MIT

# import
import quail

#load data
egg = quail.load_example_data()

#analysis
analyzed_data = quail.analyze(egg, analysis='tempclust', listgroup=['early']*8+['late']*8)
print(analyzed_data)

#plot
quail.plot(analyzed_data, title='Temporal Clustering')
