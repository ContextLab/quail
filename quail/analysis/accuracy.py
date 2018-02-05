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

    # compute recall_matrix for data slice
    recall = recall_matrix(pres_slice, rec_slice, match=match, distance=distance)

    # simple function that returns 1 if item encoded in position n is in recall list
    def compute_acc(lst):
        return len([i for i in np.unique(lst) if i>0])/(pres_slice.list_length)

    # get spc for each row in recall matrix
    acc_matrix = [compute_acc(lst) for lst in recall]

    # average over rows
    prop_recalled = np.nanmean(acc_matrix, axis=0)

    return prop_recalled
