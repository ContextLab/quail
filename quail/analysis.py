#!/usr/bin/env python
from __future__ import division
import numpy as np
import pandas as pd
from .helpers import *

def analyze_chunk(data, subjgroup=None, subjname='Subject', listgroup=None, listname='List', analysis=None, analysis_type=None, pass_features=False, **kwargs):
    """
    Private function that groups data by subject/list number and performs analysis for a chunk of data.

    Parameters
    ----------
    data : Egg data object
        The data to be analyzed

    subjgroup : list of strings or ints
        String/int variables indicating how to group over subjects.  Must be
        the length of the number of subjects

    subjname : string
        Name of the subject grouping variable

    listgroup : list of strings or ints
        String/int variables indicating how to group over list.  Must be
        the length of the number of lists

    listname : string
        Name of the list grouping variable

    analysis : function
        This function analyzes data and returns it.

    pass_features : bool
        Logical indicating whether the analyses uses the features field of the Egg

    Returns
    ----------
    analyzed_data : Pandas DataFrame
        DataFrame containing the analysis results

    """
    # if no grouping, set default to iterate over each list independently
    subjgroup = subjgroup if subjgroup else data.pres.index.levels[0].values
    listgroup = listgroup if listgroup else data.pres.index.levels[1].values

    # create a dictionary for grouping
    subjdict = {subj : data.pres.index.levels[0].values[subj==np.array(subjgroup)] for subj in set(subjgroup)}
    # listdict = {lst : data.pres.index.levels[1].values[lst==np.array(listgroup)] for lst in set(listgroup)}

    # allow for lists of listgroup arguments
    if all(isinstance(el, list) for el in listgroup):
        listdict = [{lst : data.pres.index.levels[1].values[lst==np.array(listgrpsub)] for lst in set(listgrpsub)} for listgrpsub in listgroup]
    else:
        listdict = [{lst : data.pres.index.levels[1].values[lst==np.array(listgroup)] for lst in set(listgroup)} for subj in subjdict]

    # perform the analysis
    analyzed_data = []
    for subj in subjdict:
        for lst in listdict[0]:

            # get data slice for presentation and recall
            pres_slice = data.pres.loc[[(s,l) for s in subjdict[subj] for l in listdict[subj][lst] if all(~pd.isnull(data.pres.loc[(s,l)]))]]
            pres_slice.list_length = data.list_length

            rec_slice = data.rec.loc[[(s,l) for s in subjdict[subj] for l in listdict[subj][lst] if all(~pd.isnull(data.pres.loc[(s,l)]))]]

            # if features are need for analysis, get the features for this slice of data
            if pass_features:
                feature_slice = data.features.loc[[(s,l) for s in subjdict[subj] for l in listdict[subj][lst] if all(~pd.isnull(data.pres.loc[(s,l)]))]]

            # generate indices
            index = pd.MultiIndex.from_arrays([[subj],[lst]], names=[subjname, listname])

            # perform analysis for each data chunk
            if pass_features:
                analyzed = pd.DataFrame([analysis(pres_slice, rec_slice, feature_slice, data.dist_funcs)], index=index, columns=[feature for feature in feature_slice[0].as_matrix()[0].keys()])
            elif 'n' in kwargs:
                analyzed = pd.DataFrame([analysis(pres_slice, rec_slice, n=kwargs['n'])], index=index)
            else:
                analyzed = pd.DataFrame([analysis(pres_slice, rec_slice)], index=index)

            # append analyzed data
            analyzed_data.append(analyzed)

    # concatenate slices
    analyzed_data = pd.concat(analyzed_data)

    analyzed_data.attrs = {
        'analysis_type' : analysis_type,
        'list_length' : data.list_length
    }

    for key in kwargs:
        analyzed_data.attrs[key] = kwargs[key]

    return analyzed_data

# recall matrix
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
        result = np.zeros(len(pres_list)) if len(pres_list)>=len(rec_list) else np.zeros(len(rec_list))
        result.fill(np.nan)
        for idx,rec_word in enumerate(rec_list):
            if rec_word in pres_list:
                if type(rec_word) is str:
                    result[idx]=int(pres_list.index(rec_word)+1)
        return result

    result = []
    for pres_list, rec_list in zip(presented.values, recalled.values):
        result.append(recall_pos(pres_list, rec_list))
    return result

def compute_distances(pres_list, feature_list, dist_funcs):
    """
    Compute distances between list words along n feature dimensions

    Parameters
    ----------
    pres_list : list
        list of presented words
    feature_list : list
        list of feature dicts for presented words
    dist_funcs : dict
        dict of distance functions for each feature

    Returns
    ----------
    distances : dict
        dict of distance matrices for each feature
    """

    # initialize dist dict
    distances = {}

    # for each feature in dist_funcs
    for feature in dist_funcs:

        # initialize dist matrix
        dists = np.zeros((len(pres_list), len(pres_list)))

        # for each word in the list
        for idx1, item1 in enumerate(pres_list):

            # for each word in the list
            for idx2, item2 in enumerate(pres_list):

                # compute the distance between word 1 and word 2 along some feature dimension
                dists[idx1,idx2] = dist_funcs[feature](feature_list[idx1][feature],feature_list[idx2][feature])

        # set that distance matrix to the value of a dict where the feature name is the key
        distances[feature] = dists

    return distances

def compute_feature_weights(pres_list, rec_list, feature_list, distances):
    """
    Compute clustering scores along a set of feature dimensions

    Parameters
    ----------
    pres_list : list
        list of presented words
    rec_list : list
        list of recalled words
    feature_list : list
        list of feature dicts for presented words
    distances : dict
        dict of distance matrices for each feature

    Returns
    ----------
    weights : list
        list of clustering scores for each feature dimension
    """

    # initialize the weights object for just this list
    weights = {}
    for feature in feature_list[0]:
        weights[feature] = []

    # return default list if there is not enough data to compute the fingerprint
    if len(rec_list) <= 2:
        print('Not enough recalls to compute fingerprint, returning default fingerprint.. (everything is .5)')
        for feature in feature_list[0]:
            weights[feature] = .5
        return weights

    # initialize past word list
    past_words = []
    past_idxs = []

    # loop over words
    for i in range(len(rec_list)-1):

        # grab current word
        c = rec_list[i]

        # grab the next word
        n = rec_list[i + 1]

        # if both recalled words are in the encoding list and haven't been recalled before
        if (c in pres_list and n in pres_list) and (c not in past_words and n not in past_words):

            # for each feature
            for feature in feature_list[0]:

                # get the distance vector for the current word
                dists = distances[feature][pres_list.index(c),:]

                # distance between current and next word
                cdist = dists[pres_list.index(n)]

                # filter dists removing the words that have already been recalled, and the dist for the current word
                dists_filt = np.array([dist for idx, dist in enumerate(dists) if idx not in past_idxs])

                # get indices
                avg_rank = np.mean(np.where(np.sort(dists_filt)[::-1] == cdist)[0]+1)

                # compute the weight
                weights[feature].append(avg_rank / len(dists_filt))

            # keep track of what has been recalled already
            past_idxs.append(pres_list.index(c))
            past_words.append(c)

    # average over the cluster scores for a particular dimension
    for feature in weights:
        weights[feature] = np.nanmean(weights[feature])

    return [weights[key] for key in weights]

# accuracy analysis
def accuracy_helper(pres_slice, rec_slice):
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
    recall = recall_matrix(pres_slice, rec_slice)

    # simple function that returns 1 if item encoded in position n is in recall list
    def compute_acc(lst):
        return len([i for i in np.unique(lst) if i>0])/(pres_slice.list_length)

    # get spc for each row in recall matrix
    acc_matrix = [compute_acc(lst) for lst in recall]

    # average over rows
    prop_recalled = np.mean(acc_matrix,axis=0)

    return prop_recalled

# serial position curve
def spc_helper(pres_slice, rec_slice):
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
    recall = recall_matrix(pres_slice, rec_slice)

    # get spc for each row in recall matrix
    spc_matrix = [[1 if pos in lst else 0 for pos in range(1,len(lst)+1)] for lst in recall]

    # average over rows
    prop_recalled = np.mean(spc_matrix, axis=0)

    return prop_recalled

# probability of nth recall
def pnr_helper(pres_slice, rec_slice, n):

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
    def pos_recalled_first(pos,lst,n):
        return 1 if pos==lst[n] else 0

    # get pfr for each row in recall matrix
    pnr_matrix = [[pos_recalled_first(pos,lst,n) for pos in range(1,len(lst)+1)] for lst in recall]

    # average over rows
    prob_recalled = np.mean(pnr_matrix,axis=0)

    return prob_recalled

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

# temporal clustering analysis
def tempclust_helper(pres_slice, rec_slice):
    """
    Computes temporal clustering score

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed

    Returns
    ----------
    score : float
        a number representing temporal clustering

    """

    # initialize temporal clustering list
    temporal_clustering = []

    # define distance function for temporal clustering
    dist_funcs = {
        'temporal clustering' : lambda a, b : np.abs(a-b)
    }

    # define features (just positions for temporal clustering)
    f = [{'temporal clustering' : i} for i in range(pres_slice.list_length+1)]

    # loop over lists
    for p, r in zip(pres_slice.as_matrix(), rec_slice.as_matrix()):

        # turn arrays into lists
        p = list(p)
        r = list(r)

        # compute distances
        distances = compute_distances(p, f, dist_funcs)

        # compute feature weights
        temporal_clustering.append(compute_feature_weights(p, r, f, distances))

    # return average over rows
    return np.nanmean(temporal_clustering, axis=0)

# fingerprint analysis
def fingerprint_helper(pres_slice, rec_slice, feature_slice, dist_funcs):
    """
    Computes clustering along a set of feature dimensions

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed
    feature_slice : Pandas Dataframe
        chunk of features data to be analyzed
    dist_funcs : dict
        Dictionary of distance functions for feature clustering analyses

    Returns
    ----------
    probabilities : numpy array
      each number represents clustering along a different feature dimension

    """

    # compute fingerprint for each list within a chunk
    fingerprint_matrix = []

    for p, r, f in zip(pres_slice.as_matrix(), rec_slice.as_matrix(), feature_slice.as_matrix()):

        # turn arrays into lists
        p = list(p)
        r = list(r)
        f = list(f)

        # compute distances
        distances = compute_distances(p, f, dist_funcs)

        # compute feature weights
        fingerprint_matrix.append(compute_feature_weights(p, r, f, distances))

    # return average over rows
    return np.mean(fingerprint_matrix, axis=0)

# main analysis function
def analyze(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List', analysis=None, n=0):
    """
    General analysis function that groups data by subject/list number and performs analysis.

    Parameters
    ----------
    data : Egg data object
        The data to be analyzed

    subjgroup : list of strings or ints
        String/int variables indicating how to group over subjects.  Must be
        the length of the number of subjects

    subjname : string
        Name of the subject grouping variable

    listgroup : list of strings or ints
        String/int variables indicating how to group over list.  Must be
        the length of the number of lists

    listname : string
        Name of the list grouping variable

    analysis : string
        This is the analysis you want to run.  Can be accuracy, spc, pfr,
        tempclust or fingerprint


    Returns
    ----------
    analyzed_data : Pandas DataFrame
        DataFrame containing the analysis results

    """

    # make sure an analysis is specified
    if analysis is None:
        raise ValueError('You must pass an analysis type.')

    # check if subject/list grouping variables exist on the egg
    if hasattr(data, 'subjgroup'):
        if data.subjgroup is not None:
            subjgroup = data.subjgroup

    if hasattr(data, 'subjname'):
        if data.subjname is not None:
            subjname = data.subjname

    if hasattr(data, 'listgroup'):
        if data.listgroup is not None:
            listgroup = data.listgroup

    if hasattr(data, 'listname'):
        if data.listname is not None:
            listname = data.listname

    if type(data) != list:
        data = [data]

    if type(analysis) != list:
        analysis = [analysis]

    result = [[] for d in range(len(data))]

    for idx,d in enumerate(data):
        for a in analysis:

            if a is 'accuracy':
                r = analyze_chunk(d, subjgroup=subjgroup,
                                  listgroup=listgroup,
                                  subjname=subjname,
                                  listname=listname,
                                  analysis=accuracy_helper,
                                  analysis_type='accuracy',
                                  pass_features=False)
            elif a is 'spc':
                r = analyze_chunk(d, subjgroup=subjgroup,
                                  listgroup=listgroup,
                                  subjname=subjname,
                                  listname=listname,
                                  analysis=spc_helper,
                                  analysis_type='spc',
                                  pass_features=False)
            elif a is 'pfr':
                r = analyze_chunk(d, subjgroup=subjgroup,
                                  listgroup=listgroup,
                                  subjname=subjname,
                                  listname=listname,
                                  analysis=pnr_helper,
                                  analysis_type='pfr',
                                  pass_features=False,
                                  n=0)
            elif a is 'pnr':
                r = analyze_chunk(d, subjgroup=subjgroup,
                                  listgroup=listgroup,
                                  subjname=subjname,
                                  listname=listname,
                                  analysis=pnr_helper,
                                  analysis_type='pnr',
                                  pass_features=False,
                                  n=n)
            elif a is 'lagcrp':
                r = analyze_chunk(d, subjgroup=subjgroup,
                                  listgroup=listgroup,
                                  subjname=subjname,
                                  listname=listname,
                                  analysis=lagcrp_helper,
                                  analysis_type='lagcrp',
                                  pass_features=False)
                # set indices for lagcrp
                r.columns=range(-int((len(r.columns)-1)/2),int((len(r.columns)-1)/2)+1)
            elif a is 'fingerprint':
                r = analyze_chunk(d, subjgroup=subjgroup,
                                  listgroup=listgroup,
                                  subjname=subjname,
                                  listname=listname,
                                  analysis=fingerprint_helper,
                                  analysis_type='fingerprint',
                                  pass_features=True)
            elif a is 'tempclust':
                r = analyze_chunk(d, subjgroup=subjgroup,
                                  listgroup=listgroup,
                                  subjname=subjname,
                                  listname=listname,
                                  analysis=tempclust_helper,
                                  analysis_type='tempclust')

            result[idx].append(r)

    # return analysis result
    if len(data)>1 and len(analysis)>1:
        return result
    elif len(data)>1 and len(analysis)==1:
        return [item[0] for item in result]
    elif len(data)==1 and len(analysis)>1:
        return [item for item in result[0]]
    else:
        return result[0][0]
