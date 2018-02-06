from __future__ import division
import numpy as np
from .recmat import recall_matrix

def accuracy_helper(pres_slice, rec_slice, match='exact', distance='euclidean'):
    """
    Computes proportion of words recalled

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed

    Returns
    ----------
    prop_recalled : numpy array
      proportion of words recalled

    """

    def compute_acc(lst):
        return len([i for i in np.unique(lst) if i>0])/(pres_slice.list_length)

    recmat = recall_matrix(pres_slice, rec_slice, match=match, distance=distance)

    if match in ['exact', 'best']:
        result = [compute_acc(lst) for lst in recmat]
    elif match is 'smooth':
        result = np.mean(recmat, axis=1)
    else:
        raise ValueError('Match must be set to exact, best or smooth.')

    return np.nanmean(result, axis=0)
