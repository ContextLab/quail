from __future__ import division
import warnings
import numpy as np
import six
from scipy.spatial.distance import cdist
from ..distance import dist_funcs as distdict
from ..helpers import shuffle_egg


def fingerprint_helper(egg, permute=False, n_perms=1000,
                       match='exact', distance='euclidean', features=None):
    """
    Computes clustering along a set of feature dimensions

    Parameters
    ----------
    egg : quail.Egg
        Data to analyze

    dist_funcs : dict
        Dictionary of distance functions for feature clustering analyses

    Returns
    ----------
    probabilities : Numpy array
      Each number represents clustering along a different feature dimension

    """

    if features is None:
        features = egg.dist_funcs.keys()

    inds = egg.pres.index.tolist()
    slices = [egg.crack(subjects=[i], lists=[j]) for i, j in inds]

    weights = _get_weights(slices, features, distdict, permute, n_perms, match,
                            distance)
    return np.nanmean(weights, axis=0)


def _get_corrected_rank(x, dists):
    # Legacy behavior: Average rank of matches (unnormalized? No, normalized by len)
    # dists are sorted ascending by default in numpy, but we assumed descending for 'rank'?
    # Fingerprint logic: High rank = Good match (low distance).
    # If dists=[1, 0, 0, 0] and x=0.
    # Descending: [1, 0, 0, 0]. 0 matches at indices 1, 2, 3.
    # 1-based ranks: 2, 3, 4. Avg: 3.
    # Score: 3 / 4 = 0.75.
    
    # Implementation:
    # Sort dists descending
    dists_sorted = np.sort(dists)[::-1]
    # Find indices where equal
    matches = np.where(dists_sorted == x)[0]
    if len(matches) == 0:
        return np.nan # Should not happen if x is in dists?
    
    # 1-based ranks
    ranks = matches + 1
    avg_rank = np.mean(ranks)
    return avg_rank / len(dists)


def _get_weights(slices, features, distdict, permute, n_perms, match, distance):
    weights = np.zeros((len(slices), len(features)))
    for sdx, s in enumerate(slices):
        for fdx, f in enumerate(features):
            if match == 'exact':
                weights[sdx, fdx] = _get_weight_exact(s, f, distdict, permute,
                                                      n_perms)
            elif match == 'best':
                weights[sdx, fdx] = _get_weight_best(s, f, distdict, permute,
                                                      n_perms, distance)
    return weights


def _get_weight_exact(egg, feature, distdict, permute, n_perms):

    if permute:
        return _permute(egg, feature, distdict, _get_weight_exact, n_perms)

    pres = list(egg.get_pres_items().values[0])
    rec = list(egg.get_rec_items().values[0])

    if len(rec) <= 2:
        warnings.warn('Not enough recalls to compute fingerprint, returning default'
              'fingerprint.. (everything is .5)')
        return np.nan

    distmat = get_distmat(egg, feature, distdict)

    # Map items to indices for faster lookup
    # Handle duplicate items? Quail usually assumes unique items in pres for index()
    try:
        p_map = {item: i for i, item in enumerate(pres)}
        # Filter recalls to those in presentation list
        r_idxs = [p_map[item] for item in rec if item in p_map]
    except TypeError:
        # Fallback for unhashable types (dicts/lists? shouldn't happen for items)
        r_idxs = [pres.index(item) for item in rec if item in pres]

    ranks = []
    seen = np.zeros(len(pres), dtype=bool)
    
    # Pre-loop checks
    if len(r_idxs) < 2:
        return np.nan

    for i in range(len(r_idxs)-1):
        c_idx = r_idxs[i]
        n_idx = r_idxs[i+1]
        
        # Skip if already recalled (shouldn't happen in standard FR but check)
        if seen[c_idx] or seen[n_idx]:
             # Matches logic "c not in past_words and n not in past_words"
             # If c was seen (prev iteration), it's in past.
             # Wait, loop updates past_idxs AFTER calc.
             # So c_idx is NOT seen yet.
             pass

        # Check if they were seen in *previous* steps
        if seen[c_idx] or seen[n_idx]:
            continue

        # Get distances from current item
        dists = distmat[c_idx]
        target_dist = dists[n_idx]
        
        # Filter: keep only NOT seen indices
        # Note: current c_idx is NOT in "seen" yet, so it is included in pool?
        # Original logic: "if idx not in past_idxs". past_idxs appended c AFTER.
        # So c IS in the pool?
        # "past_idxs.append(pres.index(c))" happens at end.
        valid_mask = ~seen
        valid_mask[c_idx] = False # Exclude current item from pool
        
        dists_filt = dists[valid_mask]
        
        # Optimize Rank Calculation
        # sort desc
        # n_greater = np.sum(dists_filt > target_dist)
        # n_equal = np.sum(dists_filt == target_dist)
        # avg_rank = n_greater + (n_equal + 1) / 2
        
        n_greater = np.sum(dists_filt > target_dist)
        n_equal = np.sum(dists_filt == target_dist)
        avg_rank = n_greater + (n_equal + 1) / 2.0
        
        ranks.append(avg_rank / len(dists_filt))
        
        # Update seen
        seen[c_idx] = True
        
    return np.nanmean(ranks)


def _get_weight_best(egg, feature, distdict, permute, n_perms, distance):

    if permute:
        return _permute(egg, feature, distdict, _get_weight_best, n_perms)

    rec = list(egg.get_rec_items().values[0])
    if len(rec) <= 2:
        warnings.warn('Not enough recalls to compute fingerprint, returning default'
              'fingerprint.. (everything is .5)')
        return np.nan

    distmat = get_distmat(egg, feature, distdict)
    matchmat = get_match(egg, feature, distdict)
    print(f"DEBUG: matchmat.shape={matchmat.shape}, len(rec)={len(rec)}")
    print(f"DEBUG: distmat.shape={distmat.shape}")

    ranks = []
    for i in range(len(rec)-1):
        cdx, ndx = np.argmin(matchmat[i, :]), np.argmin(matchmat[i+1, :])
        dists = distmat[cdx, :]
        di = dists[ndx]
        dists_filt = np.array([dist for idx, dist in enumerate(dists)])
        ranks.append(_get_corrected_rank(di, dists_filt))
    return np.nanmean(ranks)



def get_distmat(egg, feature, distdict):
    f_data = [xi[feature] for xi in egg.get_pres_features().values[0]]
    # Ensure (N_items, N_features)
    # If elements are scalars, np.array gives (N,), reshape to (N, 1)
    # If elements are lists, np.array gives (N, K)
    f = np.array(f_data)
    if f.ndim == 1:
        f = f.reshape(-1, 1)
        
    return cdist(f, f, distdict[egg.dist_funcs[feature]])


def get_match(egg, feature, distdict):
    p_data = [xi[feature] for xi in egg.get_pres_features().values[0]]
    p = np.array(p_data)
    if p.ndim == 1:
        p = p.reshape(-1, 1)
        
    r_data = [xi[feature] for xi in egg.get_rec_features().values[0]]
    r = np.array(r_data)
    if r.ndim == 1:
        r = r.reshape(-1, 1)
        
    return cdist(p, r, distdict[egg.dist_funcs[feature]])




def _permute(egg, feature, distdict, func, n_perms=100):
    perms = [func(shuffle_egg(egg), feature, distdict, False, None) for i in range(n_perms)]
    real = func(egg, feature, distdict, False, None)

    # permuted values that are *less* than the
    # observed value contribute a score of 1; permuted
    # values that are *equal* to the observed value contribute 0.5;
    # all others (strictly greater than) contribute 0.
    bools = [1 if perm < real else 0.5 if perm == real else 0 for perm in perms]
    return np.sum(np.array(bools), axis=0) / n_perms
