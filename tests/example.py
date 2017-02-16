# -*- coding: utf-8 -*-

from pyrec.analysis import recall_matrix
from pyrec.analysis import spc
from pyrec.analysis import pfr
from pyrec.analysis import plr
from pyrec.analysis import lag_crp
from pyrec.pyro import Pyro
import numpy as np
import pytest

presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
pyro = Pyro(pres=presented,rec=recalled)

spc_result = spc(pyro)
print(spc_result)

spc_result2 = spc(pyro, listgroup=[1,1])
print(spc_result2)

presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']],[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']],[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
multisubj_pyro = Pyro(pres=presented,rec=recalled)

spc_result = lag_crp(multisubj_pyro,listname='condition')
print(spc_result)
