from .pyro import Pyro
from .analysis import spc,pfr,plr,lag_crp
from .plot import plot

class Pyrec(object):
    '''Pyrec module'''

    def __init__(self, Pyro=Pyro, plot=plot, spc=spc,  pfr=pfr,  plr=plr, lag_crp=lag_crp):
        self.Pyro = Pyro
        self.plot = plot
        self.spc = spc
        self.pfr = pfr
        self.plr = plr
        self.lab_crp = lag_crp
