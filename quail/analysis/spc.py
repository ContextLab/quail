import numpy as np
from .recmat import recall_matrix

def spc_helper(egg, match='exact', distance='euclidean',
               features=None):
    """
    Computes probability of a word being recalled (in the appropriate recall list), given its presentation position

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
      each number represents the probability of recall for a word presented in given position/index

    """

    def spc(lst):
        d = np.zeros_like(egg.pres.values[0])
        inds = np.array(lst[~np.isnan(lst)]).astype(int)
        d[inds-1]=1
        return d

    opts = dict(match=match, distance=distance, features=features)
    if match is 'exact':
        opts.update({'features' : 'item'})
    recmat = recall_matrix(egg, **opts)

    if match in ['exact', 'best']:
        result = [spc(lst) for lst in recmat]
    elif match == 'smooth':
        result = np.nanmean(recmat, 2)
    else:
        raise ValueError('Match must be set to exact, best or smooth.')
    return np.mean(result, 0)
