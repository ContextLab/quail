import numpy as np
import pandas as pd
from .recmat import recall_matrix
from ..helpers import r2z, z2r

def lagcrp_helper(pres_slice, rec_slice, match='exact', distance='euclidean',
                  ts=None):
    """
    Computes probabilities for each transition distance (probability that a word
    recalled will be a given distance--in presentation order--from the previous
    recalled word).

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed

    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed

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

    def compute_lagcrp(rec, lstlen):
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
            for trial in range(0,lstlen-1):
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

    def compute_nlagcrp(recmat, ts=None, distance='correlation'):

        def lagcrp_model(s):
            idx = list(range(0, -s, -1))
            return np.array([list(range(i, i+s)) for i in idx])

        model = lagcrp_model(recmat.shape[1])
        lagcrp = np.zeros(ts * 2)
        for rdx in range(len(recmat)-1):
            item = recmat[rdx, :]
            next_item = recmat[rdx+1, :]
            outer = np.outer(item, next_item)
            lagcrp += np.array(list(map(lambda lag: np.mean(outer[model==lag]), range(-ts, ts))))
        lagcrp /= ts
        lagcrp = list(lagcrp)
        lagcrp.insert(int(len(lagcrp) / 2), np.nan)
        return np.array(lagcrp)

    recmat = recall_matrix(pres_slice, rec_slice, match=match, distance=distance)

    if not ts:
        ts = recmat.shape[1]

    if match in ['exact', 'best']:
        lagcrp = [compute_lagcrp(lst, pres_slice.list_length) for lst in recmat]
    elif match is 'smooth':
        lagcrp = [compute_nlagcrp(recmat, ts=ts, distance=distance)]
    else:
        raise ValueError('Match must be set to exact, best or smooth.')
    return np.nanmean(lagcrp, axis=0)
