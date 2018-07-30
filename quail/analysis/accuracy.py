from __future__ import division
import numpy as np
from .recmat import recall_matrix

def accuracy_helper(egg, match='exact', distance='euclidean',
                    features=None):
    """
    Computes proportion of words recalled

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
    prop_recalled : numpy array
      proportion of words recalled

    """

    def acc(lst):
        return len([i for i in np.unique(lst) if i>=0])/(egg.list_length)

    opts = dict(match=match, distance=distance, features=features)
    if match is 'exact':
        opts.update({'features' : 'item'})
    recmat = recall_matrix(egg, **opts)

    if match in ['exact', 'best']:
        result = [acc(lst) for lst in recmat]
    elif match is 'smooth':
        result = np.mean(recmat, axis=1)
    else:
        raise ValueError('Match must be set to exact, best or smooth.')

    return np.nanmean(result, axis=0)
