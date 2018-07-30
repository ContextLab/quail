import numpy as np
from .recmat import recall_matrix

def pnr_helper(egg, position, match='exact',
               distance='euclidean', features=None):

    """
    Computes probability of a word being recalled nth (in the appropriate recall
    list), given its presentation position.  Note: zero indexed

    Parameters
    ----------
    egg : quail.Egg
        Data to analyze

    position : int
        Position of item to be analyzed

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
    prob_recalled : numpy array
      each number represents the probability of nth recall for a word presented in given position/index

    """
    def pnr(lst, position):
        return [1 if pos==lst[position] else 0 for pos in range(1,egg.list_length+1)]

    opts = dict(match=match, distance=distance, features=features)
    if match is 'exact':
        opts.update({'features' : 'item'})
    recmat = recall_matrix(egg, **opts)

    if match in ['exact', 'best']:
        result = [pnr(lst, position) for lst in recmat]
    elif match is 'smooth':
        result = np.atleast_2d(recmat[:, :, 0])
    else:
        raise ValueError('Match must be set to exact, best or smooth.')
    return np.nanmean(result, axis=0)
