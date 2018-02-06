import numpy as np
import pandas as pd
import six
from scipy.spatial.distance import cdist
from ..helpers import check_nan

def recall_matrix(presented, recalled, match='exact', distance='euclidean'):
    """
    Computes recall matrix given list of presented and list of recalled words

    Parameters
    ----------
    presented : list of list of strings
      presentedWords are the words presented in the experiment, in order, grouped by list

    recalled : list of list of strings
      recalledWords are the words recalled by the subject, in order, grouped by list

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
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists

    """
    def _format(p, r):
        p = np.matrix([np.array(i) for i in p])
        if p.shape[0]==1:
            p=p.T
        r = map(lambda x: [np.nan]*p.shape[1] if check_nan(x) else x, r)
        r = np.matrix([np.array(i) for i in r])
        if r.shape[0]==1:
            r=r.T
        return p, r

    if isinstance(presented, pd.DataFrame):
        presented, recalled = (presented.values, recalled.values)

    result = np.empty(recalled.shape)
    for idx, (p, r) in enumerate(zip(presented, recalled)):
        if match is 'exact':
            m = [np.where(x==p)[0] for x in r]
            result[idx,:] = [x[0]+1 if len(x)>0 else np.nan for x in m]
        elif match is 'best':
            p, r = _format(p, r)
            m = 1 - cdist(r, p, distance)
            result[idx, :] = np.argmax(m, 1)+1
        elif match is 'smooth':
            p, r = _format(p, r)
            result[idx, :] = np.mean(1 - cdist(r, p, distance), 0)
    return result
