import quail
import time
import numpy as np
import pandas as pd

def run_benchmark():
    print("Generating data...")
    # 20 subjects, 10 lists each, 16 items
    n_subj = 20
    n_lists = 10
    list_len = 16
    
    # Create random items
    # Pres: ints
    pres = [[[str(k) for k in range(list_len)] for j in range(n_lists)] for i in range(n_subj)]
    # Rec: random shuffle of pres
    rec = [[[str(k) for k in np.random.permutation(range(list_len))] for j in range(n_lists)] for i in range(n_subj)]
    
    # Features: Scalar 'val'
    features = [{'item': str(k), 'val': float(k)} for k in range(list_len)]
    # Expand features to 3D
    pres_feat = [[features for j in range(n_lists)] for i in range(n_subj)]
    
    egg = quail.Egg(pres=pres, rec=rec, features=pres_feat)
    
    print("Starting fingerprint analysis...")
    start = time.time()
    # Compute fingerprint with permutations (expensive part)
    # 10 perms
    res = egg.analyze('fingerprint', n_perms=10, permute=True, parallel=False)
    end = time.time()
    
    print(f"Analysis complete in {end - start:.2f} seconds.")
    print(f"Result shape: {res.data.shape}")

if __name__ == '__main__':
    run_benchmark()
