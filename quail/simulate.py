import pandas as pd
import numpy as np
import os

def simulate_list(nwords=16, nrec=10, ncats=4):
    """A function to simulate a list"""

    # load wordpool
    # Assuming relative to this file
    path = os.path.join(os.path.dirname(__file__), 'data/cut_wordpool.csv')
    wp = pd.read_csv(path)

    # get one list
    # logic seems to pick a group random
    wp = wp[wp['GROUP']==np.random.choice(list(range(16)), 1)[0]].sample(16)

    wp['COLOR'] = [[int(np.random.rand() * 255) for i in range(3)] for i in range(16)]
    
    return wp
