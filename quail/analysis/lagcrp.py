import numpy as np
from .recmat import recall_matrix
import pandas as pd

# lag-crp
def lagcrp_helper(pres_slice, rec_slice):
    """
    Computes probabilities for each transition distance (probability that a word recalled will be a given distance--in presentation order--from the previous recalled word)

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed

    Returns
    ----------
    prob_recalled : numpy array
      each float is the probability of transition distance (distnaces indexed by position, from -(n-1) to (n-1), excluding zero

    """

    # compute recall_matrix for data slice
    recall = recall_matrix(pres_slice, rec_slice)

    def check_pair(a, b):
        if (a>0 and b>0) and (a!=b):
            return True
        else:
            return False

    def compute_actual(recall_list, list_length):
        arr=pd.Series(data=np.zeros((list_length)*2), index=list(range(-list_length,0))+list(range(1,list_length+1)))
        recalled=[]
        for trial in range(0,list_length-1):
            a=recall_list[trial]
            b=recall_list[trial+1]
            if check_pair(a, b) and (a not in recalled) and (b not in recalled):
                arr[b-a]+=1
            recalled.append(a)
        return arr

    def compute_possible(recall_list, list_length):
        arr=pd.Series(data=np.zeros((list_length)*2), index=list(range(-list_length,0))+list(range(1,list_length+1)))
        recalled=[]
        for trial in recall_list:

            if np.isnan(trial):
                pass
            else:

                low_bound=int(1-trial)
                up_bound=int(list_length-trial)

                chances=list(range(low_bound,0))+list(range(1,up_bound+1))
                #ALL transitions

                #remove transitions not possible
                for each in recalled:
                    if each-trial in chances:
                        chances.remove(each-trial)

                #update array with possible transitions
                arr[chances]+=1

                recalled.append(trial)

        return arr

    ########

    list_crp = []
    for n_list in recall:
        actual = compute_actual(n_list, pres_slice.list_length)
        possible = compute_possible(n_list, pres_slice.list_length)
        crp = [0.0 if j==0 else i/j for i,j in zip(actual,possible)]
        crp.insert(int(len(crp)/2),np.nan)
        list_crp.append(crp)

    prob_recalled = np.mean(list_crp, axis=0)

    return prob_recalled
