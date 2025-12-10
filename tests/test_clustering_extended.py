import pytest
import numpy as np
import quail
from quail.analysis.clustering import _get_corrected_rank, fingerprint_helper

def test_get_corrected_rank_logic():
    # Test descending rank logic
    # dists = [1.0, 0.5, 0.5, 0.0]
    # x = 0.5
    # Sorted Desc: [1.0, 0.5, 0.5, 0.0]
    # Indices of 0.5: 1, 2
    # Ranks: 2, 3. Avg: 2.5
    # N = 4
    # Result: 2.5/4 = 0.625
    
    dists = np.array([1.0, 0.5, 0.5, 0.0])
    x = 0.5
    # Manually compute with new function
    # Can't import private function easily without module?
    # Actually we imported it.
    
    rank = _get_corrected_rank(x, dists)
    assert np.isclose(rank, 0.625)
    
    # Test x not in dists (should return nan? or 0 matches?)
    # Implementation returns nan if len(matches)==0
    # But usually x IS in dists.
    
def test_fingerprint_helper_edge_cases():
    # 1. No recalls
    # Egg constructor pads. If we pass rec=[[]], it might become single list.
    # Ensure structure matches pres (1 subj, 1 list)
    # rec needs to be list(Subject) of list(List) of list(Items).
    # [[[]]] means Subj 0, List 0, Items [].
    egg = quail.Egg(pres=[['A', 'B']], rec=[[[]]]) 
    # If rec is empty list, it still has Subject 0, List 0.
    # Ensure crack works.
    res = fingerprint_helper(egg, features=['item'])
    # Should return nan (or warning + nan)
    # The logic returns nan if len(rec) <= 2
    # Wait, loop is len(rec)-1. Empty rec -> len 0.
    # Logic checks if len(rec) <= 2.
    assert np.all(np.isnan(res))
    
    # 2. Short recalls (1 item)
    egg = quail.Egg(pres=[['A', 'B']], rec=[['A']])
    res = fingerprint_helper(egg)
    assert np.all(np.isnan(res))
    
    # 3. Recalls not in pres
    # A B -> C D
    egg = quail.Egg(pres=[['A', 'B']], rec=[['C', 'D']])
    res = fingerprint_helper(egg)
    # Filter r_idxs will be empty.
    # Return nan.
    assert np.all(np.isnan(res))
    
    # 4. Duplicate items in pres (Logic uses first index?)
    # A A B C -> A B C
    # p_map dict will overwrite A:0 with A:1.
    # r_idxs: A->1, B->2, C->3.
    # Is this desired? Standard FR assumes unique items usually.
    # But if not unique, map picks LAST index.
    egg = quail.Egg(pres=[['A', 'A', 'B', 'C']], rec=[['A', 'B', 'C']])
    # map: A->1, B->2, C->3.
    # rec len = 3. > 2.
    # Transitions: A->B, B->C.
    # dists from 1 (second A).
    # Correct? Or undefined behavior?
    # Just ensure it doesn't crash.
    res = fingerprint_helper(egg)
    # map: A->1, B->2.
    # rec: 1, 2.
    # dists from 1 (second A).
    # Correct? Or undefined behavior?
    # Just ensure it doesn't crash.
    res = fingerprint_helper(egg)
    # numeric result
    assert not np.isnan(res)

def test_fingerprint_permute():
    # Test permutation logic runs
    pres=[['A', 'B', 'C', 'D']]
    rec=[['A', 'B', 'C', 'D']]
    egg = quail.Egg(pres=pres, rec=rec)
    
    # Run with permute=True, n_perms=10 (fast)
    res = fingerprint_helper(egg, permute=True, n_perms=10)
    # Result might be array of shape (1,) or scalar depending on return.
    # fingerprint_helper returns np.nanmean(weights, axis=0)
    # weights shape: (n_lists, n_features). If n_lists=1, n_features=1 -> (1,1).
    # nanmean axis=0 -> (1,).
    if isinstance(res, np.ndarray):
        assert res.dtype.kind == 'f'
        assert res.shape == (1,)
    else:
        assert isinstance(res, np.floating) or isinstance(res, float)
