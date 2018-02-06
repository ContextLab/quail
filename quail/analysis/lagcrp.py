import numpy as np
from .recmat import recall_matrix
import pandas as pd

# lag-crp
def lagcrp_helper(pres_slice, rec_slice, match='exact', distance='euclidean'):
    """
    Computes probabilities for each transition distance (probability that a word recalled will be a given distance--in presentation order--from the previous recalled word)

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed

    Returns
    ----------
    prob_recalled : numpy array
      each float is the probability of transition distance (distnaces indexed by position, from -(n-1) to (n-1), excluding zero

    """

    def compute_lagcrp(rec, lstlen):

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

    def compute_nlagcrp(pres, rec, ts=None, distance='correlation'):

        def lagcrp_model(s):
            idx = list(range(0, -s, -1))
            return np.array([list(range(i, i+s)) for i in idx])

        if not ts:
            ts = int(pres.shape[1]/10)

        model = lagcrp_model(ts)
        lagcrp = np.zeros(ts * 2)
        for rdx in range(len(rec)-1):
            item = 1 - cdist(rec[rdx,:].reshape(1, -1), pres, distance)
            next_item = 1 - cdist(rec[rdx+1,:].reshape(1,-1), pres, distance)
            outer = np.outer(item, next_item)
            lagcrp += np.array(list(map(lambda lag: np.mean(r2z(outer[model==lag])), range(-ts, ts))))
        lagcrp /= ts
        return z2r(lagcrp)

    if match in ['exact', 'best']:
        recall = recall_matrix(pres_slice, rec_slice, match=match,
                               distance=distance)
        lagcrp = [compute_lagcrp(lst, pres_slice.list_length) for lst in recall]
    else:
        lagcrp = [compute_nlagcrp(pres_slice, rec_slice, ts=ts,
                                  distance=distance) for lst in recall]

    return np.mean(lagcrp, axis=0)
