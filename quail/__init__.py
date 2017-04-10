from .load import load
from .egg import Egg
from .analysis import analyze
from .plot import plot
from .helpers import stack_eggs

class quail(object):
    '''quail module'''

    def __init__(self,  Egg=Egg, load=load, analyze=analyze, plot=plot, stack_eggs=stack_eggs):
        self.Egg = Egg
        self.load = load
        self.analyze = analyze
        self.plot = plot
        self.stack_eggs = stack_eggs
