# -*- coding: utf-8 -*-
"""
=============================
Plot serial position curve
=============================

This example plots the probability of recall success as a function of serial
position during stimulus encoding.

"""

# Code source: Andrew Heusser
# License: MIT

# import
import quail

#load data
egg = quail.load_example_data()

#analysis
fegg = egg.analyze('spc', listgroup=['average']*8)

#plot
fegg.plot(title='Serial Position Curve')

import json
eggd = egg.to_json()
eggd

json.dumps(eggd)
