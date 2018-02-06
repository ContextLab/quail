import numpy as np
from .recmat import recall_matrix

def pnr_helper(pres_slice, rec_slice, position, match='exact', distance='euclidean'):

    """
    Computes probability of a word being recalled nth (in the appropriate recall
    list), given its presentation position.  Note: zero indexed

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed

    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed

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
        return [1 if pos==lst[position] else 0 for pos in range(1,len(lst)+1)]

    recall = recall_matrix(pres_slice, rec_slice, match=match, distance=distance)

    if match in ['exact', 'best']:
        result = [pnr(lst, position) for lst in recall]
    elif match is 'smooth':
        result = recall
    else:
        raise ValueError('Match must be set to exact, best or smooth.')

    return np.mean(result, axis=0)
