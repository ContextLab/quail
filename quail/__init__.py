try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

from .load import load, load_example_data, load_egg, loadEL
from .egg import Egg, FriedEgg
from .analysis.analysis import analyze
from .plot import plot
from .helpers import stack_eggs, crack_egg, recmat2egg, df2list
from .decode_speech import decode_speech
from .fingerprint import Fingerprint, OptimalPresenter
from .distance import *


__version__ = version('quail')

