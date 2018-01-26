from builtins import range
import pandas
import numpy as np

def simulate_list(nwords=16, nrec=10, ncats=4):
    """A function to simulate a list"""

    # load wordpool
    wp = pd.read_csv('data/cut_wordpool.csv')

    # get one list
    wp = wp[wp['GROUP']==np.random.choice(list(range(16)), 1)[0]].sample(16)

    wp['COLOR'] = [[int(np.random.rand() * 255) for i in range(3)] for i in range(16)]
