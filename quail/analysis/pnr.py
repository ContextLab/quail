import numpy as np
from .recmat import recall_matrix

# probability of nth recall
def pnr_helper(pres_slice, rec_slice, position):

    """
    Computes probability of a word being recalled nth (in the appropriate recall
    list), given its presentation position.  Note: zero indexed

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed

    Returns
    ----------
    prob_recalled : numpy array
      each number represents the probability of nth recall for a word presented in given position/index

    """

    # compute recall_matrix for data slice
    recall = recall_matrix(pres_slice, rec_slice)

    # simple function that returns 1 if item encoded in position n is recalled first
    def pos_recalled_first(pos,lst,position):
        return 1 if pos==lst[position] else 0

    # get pfr for each row in recall matrix
    pnr_matrix = [[pos_recalled_first(pos,lst,position) for pos in range(1,len(lst)+1)] for lst in recall]

    # average over rows
    prob_recalled = np.mean(pnr_matrix, axis=0)

    return prob_recalled
