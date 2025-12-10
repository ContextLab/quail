import numpy as np
import pandas as pd
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

    def get_list_length(list_idx):
        """Get actual list length by counting non-nan items"""
        pres_row = egg.pres.iloc[list_idx]
        length = 0
        for item in pres_row:
            if isinstance(item, dict) and 'item' in item:
                if not (isinstance(item['item'], float) and pd.isna(item['item'])):
                    length += 1
                else:
                    break
            else:
                break
        return length

    def pnr(lst, position, list_idx):
        actual_length = get_list_length(list_idx)
        # Initialize with NaN for all positions up to max list length
        result = [np.nan] * egg.list_length
        # Set valid positions
        for pos in range(1, actual_length + 1):
            result[pos - 1] = 1 if pos == lst[position] else 0
        return result

    opts = dict(match=match, distance=distance, features=features)
    if match == 'exact':
        opts.update({'features' : 'item'})
    recmat = recall_matrix(egg, **opts)

    if match in ['exact', 'best']:
        result = [pnr(lst, position, i) for i, lst in enumerate(recmat)]
    elif match == 'smooth':
        result = np.atleast_2d(recmat[:, :, 0])
    else:
        raise ValueError('Match must be set to exact, best or smooth.')
    return np.nanmean(result, axis=0)
