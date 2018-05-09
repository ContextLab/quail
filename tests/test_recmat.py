# from quail.egg import Egg
# from quail.analysis.recmat import _recmat
# import numpy as np
# import pytest
#
# # generate some fake data
# stimuli = [{
#                     'item' : 'CAT',
#                     'category' : 'animal',
#                     'size' : 'bigger',
#                     'starting letter' : 'C',
#                     'length' : 3
#                  },
#                  {
#                     'item' : 'DOG',
#                     'category' : 'animal',
#                     'size' : 'bigger',
#                     'starting letter' : 'D',
#                     'length' : 3
#                  },
#                  {
#                     'item' : 'SHOE',
#                     'category' : 'object',
#                     'size' : 'smaller',
#                     'starting letter' : 'S',
#                     'length' : 4
#                  },
#                  {
#                     'item' : 'HORSE',
#                     'category' : 'animal',
#                     'size' : 'bigger',
#                     'starting letter' : 'H',
#                     'length' : 5
#                  }
# ]
# egg = Egg(pres=[stimuli], rec=[list(np.array(stimuli)[[3, 1, 0]])])
#
# def test_exact():
#     _recmat(egg.pres, egg.rec, 'exact', 'euclidean')
