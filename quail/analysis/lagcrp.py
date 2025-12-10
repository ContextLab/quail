import numpy as np
import pandas as pd
import warnings
from .recmat import recall_matrix
from scipy.spatial.distance import cdist
from ..helpers import check_nan

def lagcrp_helper(egg, match='exact', distance='euclidean',
                  ts=None, features=None):
    """
    Computes probabilities for each transition distance (probability that a word
    recalled will be a given distance--in presentation order--from the previous
    recalled word).

    Parameters
    ----------
    egg : quail.Egg
        Data to analyze

    match : str (exact, best or smooth)
        Matching approach to compute recall matrix.  If exact, the presented and
        recalled items must be identical (default).  If best, the recalled item
        that is most similar to the presented items will be selected. If smooth,
        a weighted average of all presented items will be used, where the
        weights are derived from the similarity between the recalled item and
        each presented item.

    distance : str
        The distance function used to compare presented and recalled items.
        Applies only to 'best' and 'smooth' matching approaches.  Can be any
        distance function supported by numpy.spatial.distance.cdist.

    Returns
    ----------
    prec : numpy array
      each float is the probability of transition distance (distnaces indexed by
      position, from -(n-1) to (n-1), excluding zero

    """

    def lagcrp(rec, lstlen):
        """Computes lag-crp for a given recall list (Vectorized)"""
        # rec is a list/array of item INDICES.
        # Quail's recall_matrix returns 1-based indices (1..L).
        # NaNs are empty/missing.
        # 0 might represent intrusions (from docstring: "0s represent recalled words not presented").
        
        # Filter valid recalls: must be integer > 0 and <= lstlen (since we only enable lags for within-list items)
        # Convert to 0-based index: item - 1.
        
        valid_mask = ~np.isnan(rec)
        rec_arr = np.array(rec)[valid_mask].astype(int)
        
        # Keep only items in range [1, lstlen]
        # (Handling intrusions typically excludes them from LagCRP?)
        in_range = (rec_arr >= 1) & (rec_arr <= lstlen)
        rec = rec_arr[in_range] - 1
        
        if len(rec) < 2:
            # Need at least 2 items for a transition
            # Return array of NaNs for all possible lags (-L..-1, 1..L)
            # Length = 2*L + 1 (including 0 lag which is also NaN) or 2*L?
            # Legacy returned 2*L+1 (with 0-lag as NaN)
            res = np.full(lstlen * 2 + 1, np.nan)
            return res

        # Actual transitions
        # lags = rec[i+1] - rec[i]
        actual_lags = rec[1:] - rec[:-1]
        
        # Possible transitions
        # For each step i (from 0 to N-2), we are at rec[i].
        # What items could we go to?
        # Any item k in 0..lstlen-1 that is NOT already recalled (rec[:i+1])
        # Because standard CRP assumes sampling without replacement (for free recall).
        
        # We need to compute the set of possible lags for each transition.
        # possible_lags[i] = { k - rec[i] for k in 0..L-1 if k not in rec[:i+1] }
        
        # Optimization:
        # Instead of iterating, can we use broadcasting?
        # Matrix of all possible transitions from current item:
        # current_items = rec[:-1] (size N-1)
        # all_items = np.arange(lstlen)
        # raw_lags = all_items[None, :] - current_items[:, None]  (Shape: N-1, L)
        
        # Now mask out items that were already recalled.
        # recalled_mask[i, k] = True if item k was recalled at or before step i.
        # We can build this mask.
        
        # Create a mask of (N-1, L).
        # For step i, we want to know if item k is in rec[:i+1].
        # rec[:i+1] includes current item rec[i]. 
        # So we cannot transition to ourselves (0 lag) or any previous item.
        
        # Let's verify legacy behavior: "if check_pair(a, b) and (a not in recalled) and (b not in recalled):"
        # Wait, legacy check_pair says: (a>0 and b>0) and (a!=b). 
        # And "b not in recalled_so_far".
        # Legacy loop:
        # for trial in range(0,len(rec)-1):
        #   a=rec[trial]; b=rec[trial+1]
        #   recalled.append(a)
        #   if ... b not in recalled ...
        # Actually legacy `recalled` is appended AFTER the check?
        # Line 58: recalled.append(a) is AFTER check.
        # So at step i (transition a->b), `recalled` contains items 0..i-1. 
        # `a` is rec[i]. `b` is rec[i+1].
        # The check `b not in recalled` means b must not have been recalled BEFORE `a`.
        # This is standard CRP (cannot transition to already recalled).
        
        # Constructing validity mask:
        # Mask shape (N-1, L).
        # We want mask[i, k] = True if item k is AVAILABLE (not recalled yet).
        # rec_indices = rec[:-1]
        
        # Matrix of when each item was recalled?
        # recall_positions = np.full(lstlen, np.inf)
        # recall_positions[rec] = np.arange(len(rec))
        # But we only care about the *first* time an item is recalled for availability?
        # Actually if an item is recalled twice, it's weird. Assuming unique recalls for now.
        
        # Efficient mask construction:
        # mask = np.ones((len(rec)-1, lstlen), dtype=bool)
        # For each step i, items in rec[:i] are unavailable.
        # Also item rec[i] is unavailable (cannot self-transition).
        # This implies a cumulative structure.
        
        # Broadcasting strategy:
        # We track "unavailable" items.
        # unavailable_mask = np.zeros((len(rec)-1, lstlen), dtype=bool)
        # We can fill this by iterating the shorter dimension (timesteps, usually <30) which is fast enough,
        # or use `np.tri` tricks if purely index-based.
        # Since recall order is arbitrary (permutations of indices), `np.tri` doesn't apply directly to content.
        # But we can use `np.add.accumulate` on a one-hot representation!
        
        # One-hot encoding of recalls:
        # matrix (N_rec, L). 1 at [t, item_t].
        one_hot = np.zeros((len(rec), lstlen), dtype=int)
        one_hot[np.arange(len(rec)), rec] = 1
        
        # Cumulative recalls (items recalled up to step t):
        # cum_recalls = np.cumsum(one_hot, axis=0)
        # At step i (transition from i to i+1), items unavailable are those recalled at 0..i.
        # unavailable_at_i = cum_recalls[i]
        # (This assumes unique recalls - if repeats, >1, still unavailable).
        
        # We need denominator for steps 0..N-2.
        # So we use cum_recalls[0..N-2].
        cum_recalls = np.cumsum(one_hot, axis=0)
        unavailable = cum_recalls[:-1] > 0
        
        # Current items at each step 0..N-2 (from)
        current = rec[:-1]
        
        # Possible lags for step i: (0..L-1) - current[i]
        # We want to count frequencies of these lags WHERE item is available.
        
        # Create matrix of lags:
        # lags[i, k] = k - current[i]
        all_idxs = np.arange(lstlen)
        lags_matrix = all_idxs[None, :] - current[:, None] # Shape (N-1, L)
        
        # Mask valid transitions
        # We also need to exclude "self" (lag 0). Is self in unavailable?
        # cum_recalls[i] includes rec[i]. So yes, rec[i] is marked unavailable.
        # So ~unavailable gives us valid destinations.
        valid_mask = ~unavailable
        
        # Compute "Possible" counts per lag
        # We flat the lags_matrix and using weights from valid_mask (0 or 1)
        # We want histogram of lags_matrix elements weighted by valid_mask.
        
        possible_lags_flat = lags_matrix.ravel()
        weights_flat = valid_mask.ravel().astype(int)
        
        # Possible counts
        # Range of lags is -(L-1) to (L-1).
        # We can use np.bincount with offset.
        # strict lag range: -lstlen+1 to lstlen-1.
        # But for array indexing let's shift by lstlen.
        time_bins = np.arange(-lstlen, lstlen+1) # Includes endpoints for histogram
        
        # We can just iterate the bins or use bincount?
        # bincount requires non-negative ints.
        # Offset lags by lstlen.
        offset = lstlen
        possible_counts = np.bincount(possible_lags_flat + offset, weights=weights_flat, minlength=2*lstlen+1)
        
        # Actual counts
        # actual_lags are 1D array.
        actual_counts = np.bincount(actual_lags + offset, minlength=2*lstlen+1)
        
        # Compute CRP
        # Indices in result: -lstlen .. lstlen.
        # bincount index x corresponds to lag (x - offset).
        # We want output format: list of probs for lags [-L, -L+1, ..., -1, 1, ..., L]
        # Index 0 is -L (lag -L occurs? min lag is -(L-1)). 
        # Legacy code returns size 2*L + 1 (last elem is for lag L? No, ranges are asymmetric?)
        # Legacy: index=list(range(-lstlen,0))+list(range(1,lstlen+1))
        # Total 2*lstlen items. Plus inserted NaN at midpoint.
        # range(-lstlen, 0) -> -lstlen ... -1 (len L)
        # range(1, lstlen+1) -> 1 ... lstlen (len L)
        # Total 2L. Midpoint 0 inserted later.
        
        # Slice our counts.
        # Index corresponding to lag k is k + lstlen.
        # We want lags -lstlen ... -1  ==> indices 0 ... lstlen-1
        # We want lags 1 ... lstlen ==> indices lstlen+1 ... 2*lstlen
        
        # Note: lag -lstlen is impossible (min lag -(L-1)). But legacy includes it (value 0).
        
        with np.errstate(divide='ignore', invalid='ignore'):
            crp_ratio = actual_counts / possible_counts
            
        # Legacy behavior: if possible count is 0, return 0.0 (instead of NaN/Inf)
        # crp_ratio[possible_counts == 0] = 0.0  # Or using nan_to_num after division if NaNs produced
        
        # Replace NaNs/Infs with 0
        crp_ratio[~np.isfinite(crp_ratio)] = 0.0
            
        # Select relevant parts
        # 0..lstlen-1 (Left part)
        # lstlen+1..2*lstlen (Right part)
        # Skip lstlen (which is lag 0)
        
        # Construct result
        # To match legacy: [neg_lags ..., nan, pos_lags ...]
        res_left = crp_ratio[0:lstlen]
        res_right = crp_ratio[lstlen+1:2*lstlen+1]
        
        # Combine
        res = np.concatenate([res_left, [np.nan], res_right])
        
        return res

    def nlagcrp(distmat, ts=None):

        def lagcrp_model(s):
            idx = list(range(0, -s, -1))
            return np.array([list(range(i, i+s)) for i in idx])

        # remove nan columns
        distmat = distmat[:,~np.all(np.isnan(distmat), axis=0)].T

        model = lagcrp_model(distmat.shape[1])
        lagcrp = np.zeros(ts * 2)
        for rdx in range(len(distmat)-1):
            item = distmat[rdx, :]
            next_item = distmat[rdx+1, :]
            if not np.isnan(item).any() and not np.isnan(next_item).any():
                outer = np.outer(item, next_item)
                lagcrp += np.array(list(map(lambda lag: np.mean(outer[model==lag]), range(-ts, ts))))
        lagcrp /= ts
        lagcrp = list(lagcrp)
        lagcrp.insert(int(len(lagcrp) / 2), np.nan)
        return np.array(lagcrp)

    def _format(p, r):
        p = np.matrix([np.array(i) for i in p])
        if p.shape[0]==1:
            p=p.T
        r = map(lambda x: [np.nan]*p.shape[1] if check_nan(x) else x, r)
        r = np.matrix([np.array(i) for i in r])
        if r.shape[0]==1:
            r=r.T
        return p, r

    opts = dict(match=match, distance=distance, features=features)
    if match == 'exact':
        opts.update({'features' : 'item'})
    recmat = recall_matrix(egg, **opts)
    if not ts:
        ts = egg.pres.shape[1]
    if match in ['exact', 'best']:
        lagcrp = [lagcrp(lst, egg.list_length) for lst in recmat]
    elif match == 'smooth':
        lagcrp = np.atleast_2d(np.mean([nlagcrp(r, ts=ts) for r in recmat], 0))
    else:
        raise ValueError('Match must be set to exact, best or smooth.')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        return np.nanmean(lagcrp, axis=0)
