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
cracked_egg = quail.crack_egg(egg, subjects=[0], lists=[0])

cracked_egg.info()

pres = cracked_egg.get_pres_items().as_matrix()[0]
rec = cracked_egg.get_rec_items().as_matrix()[0]

def distmat(egg, feature, distdict):
    f = [xi[feature] for xi in egg.get_pres_features()]
    return cdist(f, f, distdict[feature])


for idx in range(len(rec)-1):
    ind1 = np.where(pres==rec[idx])[0][0]
    ind2 = np.where(pres==rec[idx+1])[0][0]
    dists = dist[ind1, :]
    cdist = dist[ind1, ind2]
    rank = np.mean(np.where(np.sort(dists)[::-1] == cdist))
