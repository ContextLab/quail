from .pyro import Pyro
from .analysis import analyze,spc,pfr,plr,lagcrp,fingerprint
from .plot import plot

class Pyrec(object):
    '''Pyrec module'''

    def __init__(self, Pyro=Pyro, analyze=analyze, plot=plot, spc=spc,  pfr=pfr,  plr=plr, lagcrp=lagcrp, fingerprint=fingerprint):
        self.Pyro = Pyro
        self.analyze = analyze
        self.plot = plot
        self.spc = spc
        self.pfr = pfr
        self.plr = plr
        self.lagcrp = lagcrp
        self.fingerprint = fingerprint
