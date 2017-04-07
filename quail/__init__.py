from .load import load
from .egg import Egg
from .analysis import analyze
from .plot import plot
from .helpers import stack_eggs

class quail(object):
    '''quail module'''

    def __init__(self, load=load, Egg=Egg, analyze=analyze, plot=plot, stack_eggs=stack_eggs):
        self.load = load
        self.Egg = Egg
        self.analyze = analyze
        self.plot = plot
