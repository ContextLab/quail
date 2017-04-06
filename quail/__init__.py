from .egg import Egg
from .analysis import analyze,spc,pfr,lagcrp,fingerprint
from .plot import plot

class quail(object):
    '''quail module'''

    def __init__(self, Egg=Egg, analyze=analyze, plot=plot, spc=spc,  pfr=pfr, lagcrp=lagcrp, fingerprint=fingerprint):
        self.Egg = Egg
        self.analyze = analyze
        self.plot = plot
        self.spc = spc
        self.pfr = pfr
        self.lagcrp = lagcrp
        self.fingerprint = fingerprint
