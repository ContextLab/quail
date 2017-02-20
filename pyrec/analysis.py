#!/usr/bin/env python

from __future__ import division
import numpy as np
import pandas as pd
from .helpers import *

def analyze(data, subjgroup=None, subjname='Subject', listgroup=None, listname='List', analysis=None, analysis_type=None):
    """
    General analysis function that groups data by subject/list number and performs analysis.

    Parameters
    ----------
    data : pyro data object
        The data to be analyzed

    subjgroup : list of strings or ints
        String/int variables indicating how to group over subjects.  Must be
        the length of the number of subjects

    listgroup : list of strings or ints
        String/int variables indicating how to group over list.  Must be
        the length of the number of lists

    analysis : function
        This function analyzes data and returns it

    Returns
    ----------
    analyzed_data : pyro data object
        Pyro containing the analysis results

    """
    # if no grouping, set default to iterate over each list independently
    subjgroup = subjgroup if subjgroup else data.pres.index.levels[0].values
    listgroup = listgroup if listgroup else data.pres.index.levels[1].values

    # create a dictionary for grouping
    subjdict = {subj : data.pres.index.levels[0].values[subj==np.array(subjgroup)] for subj in set(subjgroup)}
    listdict = {lst : data.pres.index.levels[1].values[lst==np.array(listgroup)] for lst in set(listgroup)}

    # perform the analysis
    analyzed_data = []
    for subj in subjdict:
        for lst in listdict:

            # get data slice for presentation and recall
            pres_slice = data.pres.loc[[(s,l) for s in subjdict[subj] for l in listdict[lst]]]
            rec_slice = data.rec.loc[[(s,l) for s in subjdict[subj] for l in listdict[lst]]]

            # compute recall_matrix for data slice
            recall = recall_matrix(pres_slice, rec_slice)

            # generate index
            index = pd.MultiIndex.from_arrays([[subj],[lst]], names=[subjname, listname])

            # perform analysis for each data chunk
            analyzed = pd.DataFrame([analysis(recall)], index=index)

            # append analyzed data
            analyzed_data.append(analyzed)

    # concatenate slices
    analyzed_data = pd.concat(analyzed_data)

    # add the analysis type for smart plotting
    analyzed_data.analysis_type = analysis_type

    return analyzed_data

##RECALL MATRIX#######

def recall_matrix(presented, recalled):
    """
    Computes recall matrix given list of presented and list of recalled words

    Parameters
    ----------
    presented : list of list of strings
      presentedWords are the words presented in the experiment, in order, grouped by list

    recalled : list of list of strings
      recalledWords are the words recalled by the subject, in order, grouped by list

    Returns
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists

    """

    def recall_pos(pres_list,rec_list):
        pres_list = list(pres_list)
        rec_list = list(rec_list)
        result = np.zeros(len(pres_list))
        result.fill(np.nan)
        for idx,rec_word in enumerate(rec_list):
            if rec_word in pres_list:
                result[idx]=int(pres_list.index(rec_word)+1)

        # [int(pres_list.index(rec_word)+1) if rec_word in pres_list else np.nan for rec_word in rec_list]
        return result

    result = []
    for pres_list, rec_list in zip(presented.values, recalled.values):
        result.append(recall_pos(pres_list, rec_list))

    return result

def spc_helper(recall_matrix):
    """
    Computes probability of a word being recalled (in the appropriate recall list), given its presentation position

    Parameters
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists

    Returns
    ----------
    probabilities : numpy array of ints
      each int represents the probability of recall for a word presented in given position/index

    """

    # simple function that returns 1 if item encoded in position n is in recall list
    def pos_in_list(pos,lst):
        return 1 if pos in lst else 0

    # get spc for each row in recall matrix
    spc_matrix = [[pos_in_list(pos,lst) for pos in range(1,len(lst)+1)] for lst in recall_matrix]

    # average over rows
    return np.mean(spc_matrix,axis=0)

#PROB FIRST RECALL######

def pfr_helper(recall_matrix):

    """
    Computes probability of a word being recalled first (in the appropriate recall list), given its presentation position

    Parameters
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists

    Returns
    ----------
    probabilities : numpy array of ints
      each int represents the probability of first recall for a word presented in given position/index

    """

    # simple function that returns 1 if item encoded in position n is recalled first
    def pos_recalled_first(pos,lst):
        return 1 if pos==lst[0] else 0

    # get pfr for each row in recall matrix
    pfr_matrix = [[pos_recalled_first(pos,lst) for pos in range(1,len(lst)+1)] for lst in recall_matrix]

    # average over rows
    return np.mean(pfr_matrix,axis=0)

def plr_helper(recall_matrix):
    """
    Computes probability of a word being recalled last (in the appropriate recall list), given its presentation position

    Parameters
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists

    Returns
    ----------
    probabilities : numpy array of ints
      each int represents the probability of last recall for a word presented in given position/index

    """

    # simple function that returns 1 if item encoded in position n is recalled last
    def pos_recalled_last(pos,lst):
        idx=-1
        while np.isnan(lst[idx]):
            idx-=1
        return 1 if pos==lst[idx] else 0

    # get plr for each row in recall matrix
    plr_matrix = [[pos_recalled_last(pos,lst) for pos in range(1,len(lst)+1)] for lst in recall_matrix]

    # average over rows
    return np.mean(plr_matrix,axis=0)

def crp_helper(recall_matrix):
    """
    Computes probabilities for each transition distance (probability that a word recalled will be a given distance--in presentation order--from the previous recalled word)

    Parameters
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists

    Returns
    ----------
    probabilities : list of floats
      each float is the probability of transition distance (distnaces indexed by position, from -(n-1) to (n-1), excluding zero

    """

    def check_pair(a, b):
        if (a>0 and b>0) and (a!=b):
            return True
        else:
            return False

    def compute_actual(recall_list):
        length=len(recall_list)
        arr=pd.Series(data=np.zeros((length-1)*2), index=list(range(1-length,0))+list(range(1,length)))
        recalled=[]
        for trial in range(0,length-1):
            a=recall_list[trial]
            b=recall_list[trial+1]
            if check_pair(a, b) and (a not in recalled) and (b not in recalled):
                arr[b-a]+=1
            recalled.append(a)
        return arr

    def compute_possible(recall_list):

        length=len(recall_list)
        arr=pd.Series(data=np.zeros((length-1)*2), index=list(range(1-length,0))+list(range(1,length)))

        recalled=[]
        for trial in recall_list:

            if np.isnan(trial):
                pass
            else:

                low_bound=1-trial
                up_bound=length-trial

                chances=list(range(low_bound,0))+list(range(1,up_bound+1))
                #ALL transitions


                #remove transitions not possible
                for each in recalled:
                    chances.remove(each-trial)


                #update array with possible transitions
                arr[chances]+=1

                recalled.append(trial)

        return arr

    ########

    list_crp = []
    for n_list in recall_matrix:
        actual = compute_actual(n_list)
        possible = compute_possible(n_list)

        list_crp.append([0.0 if i==0 and j==0 else i/j for i,j in zip(actual,possible)])
        #if actual and possible are both zero, append zero; otherwise, divide

    return np.mean(list_crp, axis=0)

def spc(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List'):
    return analyze(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=spc_helper, analysis_type='spc')

def pfr(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List'):
    return analyze(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=pfr_helper, analysis_type='pfr')

def plr(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List'):
    return analyze(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=plr_helper, analysis_type='plr')

def lag_crp(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List'):
    return analyze(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=crp_helper, analysis_type='lag_crp')
