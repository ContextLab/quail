import numpy as np
from .recmat import recall_matrix

def spc_helper(pres_slice, rec_slice, match='exact', distance='euclidean'):
    """
    Computes probability of a word being recalled (in the appropriate recall list), given its presentation position

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
    prop_recalled : numpy array
      each number represents the probability of recall for a word presented in given position/index

    """

    def spc(lst):
        return [1 if pos in lst else 0 for pos in range(1,len(lst)+1)]

    recall = recall_matrix(pres_slice, rec_slice, match=match, distance=distance)

    print(recall)

    if match in ['exact', 'best']:
        result = [spc(lst) for lst in recall]
    else:
        result = recall

    return np.nanmean(result, axis=0)
