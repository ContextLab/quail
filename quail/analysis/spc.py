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

    Returns
    ----------
    prop_recalled : numpy array
      each number represents the probability of recall for a word presented in given position/index

    """

    # compute recall_matrix for data slice
    recall = recall_matrix(pres_slice, rec_slice, match=match, distance=distance)

    # get spc for each row in recall matrix
    if match in ['exact', 'best']:
        spc_matrix = [[1 if pos in lst else 0 for pos in range(1,len(lst)+1)] for lst in recall]
    else:
        spc_matrix = recall

    # average over rows
    prop_recalled = np.nanmean(spc_matrix, axis=0)
    print(prop_recalled)

    return prop_recalled
