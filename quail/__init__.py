from .load import load, load_example_data
from .egg import Egg
from .analysis import analyze
from .plot import plot
from .helpers import stack_eggs
<<<<<<< HEAD
from .helpers import crack_egg
from .helpers import recmat2egg
from .helpers import load_egg
=======
>>>>>>> 1c1cb6480053abca7d818eaa4838a1c24d6fe7fd
from decode_speech import decode_speech

class quail(object):
    '''quail module'''

<<<<<<< HEAD
    def __init__(self,  Egg=Egg, load=load, load_example_data=load_example_data,
                 analyze=analyze, plot=plot, stack_eggs=stack_eggs,
                 crack_egg=crack_egg, recmat2egg=recmat2egg, load_egg=load_egg,
                 decode_speech=decode_speech):

=======
    def __init__(self,  Egg=Egg, load=load, load_example_data=load_example_data, analyze=analyze, plot=plot, stack_eggs=stack_eggs, decode_speech=decode_speech):
>>>>>>> 1c1cb6480053abca7d818eaa4838a1c24d6fe7fd
        self.Egg = Egg
        self.load = load
        self.load_example_data = load_example_data
        self.analyze = analyze
        self.plot = plot
        self.stack_eggs = stack_eggs
<<<<<<< HEAD
        self.crack_egg = crack_egg
        self.recmat2egg = recmat2egg
        self.load_egg = load_egg
=======
>>>>>>> 1c1cb6480053abca7d818eaa4838a1c24d6fe7fd
        self.decode_speech = decode_speech
