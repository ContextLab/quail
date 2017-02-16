from .pyro import Pyro
from .analysis import spc,pfr,plr,lag_crp

class Pyrec(object):
    '''Pyrec module'''

    def __init__(self, Pyro=Pyro, spc=spc,  pfr=pfr,  plr=plr, lag_crp=lag_crp):
        self.Pyro = Pyro
        self.spc = spc
        self.pfr = pfr
        self.plr = plr
        self.lab_crp = lag_crp
