from .pyro import Pyro
from .analysis import spc,pfr,plr,lagcrp
from .plot import plot

class Pyrec(object):
    '''Pyrec module'''

    def __init__(self, Pyro=Pyro, plot=plot, spc=spc,  pfr=pfr,  plr=plr, lagcrp=lagcrp):
        self.Pyro = Pyro
        self.plot = plot
        self.spc = spc
        self.pfr = pfr
        self.plr = plr
        self.lagcrp = lagcrp
