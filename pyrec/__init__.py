from .pyro import Pyro
from .analysis import analyze,spc,pfr,lagcrp,fingerprint
from .plot import plot

class Pyrec(object):
    '''Pyrec module'''

    def __init__(self, Pyro=Pyro, analyze=analyze, plot=plot, spc=spc,  pfr=pfr, lagcrp=lagcrp, fingerprint=fingerprint):
        self.Pyro = Pyro
        self.analyze = analyze
        self.plot = plot
        self.spc = spc
        self.pfr = pfr
        self.lagcrp = lagcrp
        self.fingerprint = fingerprint
