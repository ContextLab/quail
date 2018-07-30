import numpy as np
import pandas as pd
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
        """Computes lag-crp for a given recall list"""

        def check_pair(a, b):
            if (a>0 and b>0) and (a!=b):
                return True
            else:
                return False

        def compute_actual(rec, lstlen):
            arr=pd.Series(data=np.zeros((lstlen)*2),
                          index=list(range(-lstlen,0))+list(range(1,lstlen+1)))
            recalled=[]
            for trial in range(0,len(rec)-1):
                a=rec[trial]
                b=rec[trial+1]
                if check_pair(a, b) and (a not in recalled) and (b not in recalled):
                    arr[b-a]+=1
                recalled.append(a)
            return arr

        def compute_possible(rec, lstlen):
            arr=pd.Series(data=np.zeros((lstlen)*2),
                          index=list(range(-lstlen,0))+list(range(1,lstlen+1)))
            recalled=[]
            for trial in rec:
                if np.isnan(trial):
                    pass
                else:
                    lbound=int(1-trial)
                    ubound=int(lstlen-trial)
                    chances=list(range(lbound,0))+list(range(1,ubound+1))
                    for each in recalled:
                        if each-trial in chances:
                            chances.remove(each-trial)
                    arr[chances]+=1
                    recalled.append(trial)
            return arr

        actual = compute_actual(rec, lstlen)
        possible = compute_possible(rec, lstlen)
        crp = [0.0 if j == 0 else i / j for i, j in zip(actual, possible)]
        crp.insert(int(len(crp) / 2), np.nan)
        return crp

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
    if match is 'exact':
        opts.update({'features' : 'item'})
    recmat = recall_matrix(egg, **opts)
    if not ts:
        ts = egg.pres.shape[1]
    if match in ['exact', 'best']:
        lagcrp = [lagcrp(lst, egg.list_length) for lst in recmat]
    elif match is 'smooth':
        lagcrp = np.atleast_2d(np.mean([nlagcrp(r, ts=ts) for r in recmat], 0))
    else:
        raise ValueError('Match must be set to exact, best or smooth.')
    return np.nanmean(lagcrp, axis=0)
