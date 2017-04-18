from .load import load, load_example_data
from .egg import Egg
from .analysis import analyze
from .plot import plot
from .helpers import stack_eggs
from decode_speech import decode_speech

class quail(object):
    '''quail module'''

    def __init__(self,  Egg=Egg, load=load, load_example_data=load_example_data, analyze=analyze, plot=plot, stack_eggs=stack_eggs, decode_speech=decode_speech):
        self.Egg = Egg
        self.load = load
        self.load_example_data = load_example_data
        self.analyze = analyze
        self.plot = plot
        self.stack_eggs = stack_eggs
        self.decode_speech = decode_speech
