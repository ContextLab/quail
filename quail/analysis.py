#!/usr/bin/env python

from __future__ import division
import numpy as np
import pandas as pd
from .helpers import *

def analyze_chunk(data, subjgroup=None, subjname='Subject', listgroup=None, listname='List', analysis=None, analysis_type=None, pass_features=False):
    """
    General analysis function that groups data by subject/list number and performs analysis.

    Parameters
    ----------
    data : egg data object
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
    analyzed_data : egg data object
        Egg containing the analysis results

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

            # if features are need for analysis, get the features for this slice of data
            if pass_features:
                feature_slice = data.features.loc[[(s,l) for s in subjdict[subj] for l in listdict[lst]]]

            # generate index
            index = pd.MultiIndex.from_arrays([[subj],[lst]], names=[subjname, listname])

            # perform analysis for each data chunk
            if pass_features:
                analyzed = pd.DataFrame([analysis(pres_slice, rec_slice, feature_slice, data.dist_funcs)], index=index, columns=[feature for feature in feature_slice[0].as_matrix()[0].keys()])
            else:
                analyzed = pd.DataFrame([analysis(pres_slice, rec_slice)], index=index)

            # append analyzed data
            analyzed_data.append(analyzed)

    # concatenate slices
    analyzed_data = pd.concat(analyzed_data)

    # add the analysis type for smart plotting
    analyzed_data.analysis_type = analysis_type

    # add the analysis type for smart plotting
    analyzed_data.list_length = data.list_length

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
        result = np.zeros(len(pres_list)) if len(pres_list)>=len(rec_list) else np.zeros(len(rec_list))
        result.fill(np.nan)
        for idx,rec_word in enumerate(rec_list):
            if rec_word in pres_list:
                if type(rec_word) is str:
                    result[idx]=int(pres_list.index(rec_word)+1)

        # [int(pres_list.index(rec_word)+1) if rec_word in pres_list else np.nan for rec_word in rec_list]
        return result

    result = []
    for pres_list, rec_list in zip(presented.values, recalled.values):
        result.append(recall_pos(pres_list, rec_list))
    return result

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
        return len([i for i in lst if i>0])/len(lst)

    # get spc for each row in recall matrix
    acc_matrix = [compute_acc(lst) for lst in recall]

    # average over rows
    prop_recalled = np.mean(acc_matrix,axis=0)

    return prop_recalled

def spc_helper(pres_slice, rec_slice):
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
    prop_recalled : numpy array
      each number represents the probability of recall for a word presented in given position/index

    """

    # compute recall_matrix for data slice
    recall = recall_matrix(pres_slice, rec_slice)

    # simple function that returns 1 if item encoded in position n is in recall list
    def pos_in_list(pos,lst):
        return 1 if pos in lst else 0

    # get spc for each row in recall matrix
    spc_matrix = [[pos_in_list(pos,lst) for pos in range(1,len(lst)+1)] for lst in recall]

    # average over rows
    prop_recalled = np.mean(spc_matrix,axis=0)

    return prop_recalled

#PROB FIRST RECALL######

def pfr_helper(pres_slice, rec_slice):

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
    prob_recalled : numpy array
      each number represents the probability of first recall for a word presented in given position/index

    """

    # compute recall_matrix for data slice
    recall = recall_matrix(pres_slice, rec_slice)

    # simple function that returns 1 if item encoded in position n is recalled first
    def pos_recalled_first(pos,lst):
        return 1 if pos==lst[0] else 0

    # get pfr for each row in recall matrix
    pfr_matrix = [[pos_recalled_first(pos,lst) for pos in range(1,len(lst)+1)] for lst in recall]

    # average over rows
    prob_recalled = np.mean(pfr_matrix,axis=0)

    return prob_recalled

def lagcrp_helper(pres_slice, rec_slice):
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

                low_bound=int(1-trial)
                up_bound=int(length-trial)

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
        actual = compute_actual(n_list)
        possible = compute_possible(n_list)
        crp = [0.0 if i==0 and j==0 else i/j for i,j in zip(actual,possible)]
        crp = crp[:int(round(len(crp)/2))]+[np.nan]+crp[int(round(len(crp)/2)):]
        list_crp.append(crp)

    prob_recalled = np.mean(list_crp, axis=0)

    return prob_recalled


def fingerprint_helper(pres_slice, rec_slice, feature_slice, dist_funcs):
    """
    Computes clustering along a set of feature dimensions

    Parameters
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists

    Returns
    ----------
    probabilities : numpy array
      each number represents clustering along a different feature dimension

    """

    def compute_distances(pres_list, feature_list, dist_funcs):

        # initialize distance dictionary
        distances = []
        for idx,word in enumerate(pres_list):
            stimulus = {}
            stimulus['word'] = word
            stimulus['distances'] = {}
            for feature in feature_list[idx]:
                stimulus['distances'][feature] = []
            distances.append(stimulus)

        # loop over the lists to create distance matrices
        for i,stimulus1 in enumerate(feature_list):
            for j,stimulus2 in enumerate(feature_list):
                for feature in stimulus1:
                    distances[i]['distances'][feature].append({
                            'word' : distances[j]['word'],
                            'dist' : dist_funcs[feature](stimulus1[feature],stimulus2[feature])
                        })

        return distances

    def compute_feature_weights(pres_list, rec_list, feature_list, distances):

        # initialize the weights object for just this list
        listWeights = {}
        for feature in feature_list[0]:
            listWeights[feature] = []

        # return default list if there is not enough data to compute the fingerprint
        if len(rec_list) <= 2:
            print('Not enough recalls to compute fingerprint, returning default fingerprint.. (everything is .5)')
            for feature in feature_list[0]:
                listWeights[feature] = .5
            return listWeights

        # initialize pastWords list
        pastWords = []

        # finger print analysis
        for i in range(0,len(rec_list)-1):

            # grab current word
            currentWord = rec_list[i]

            # grab the next word
            nextWord = rec_list[i + 1]

            # grab the words from the encoding list
            encodingWords = pres_list

            # append current word to past words log
            # pastWords.append(currentWord)

            # if both recalled words are in the encoding list
            if (currentWord in encodingWords and nextWord in encodingWords) and (currentWord not in pastWords and nextWord not in pastWords):
                # print(currentWord,nextWord,encodingWords,pastWords)

                for feature in feature_list[0]:

                    # get the distance vector for the current word
                    distVec = distances[encodingWords.index(currentWord)]['distances'][feature]

                    # filter distVec removing the words that have already been analyzed from future calculations
                    filteredDistVec = []
                    for word in distVec:
                        if word['word'] in pastWords:
                            pass
                        else:
                            filteredDistVec.append(word)

                    # sort distWords by distances
                    filteredDistVec = sorted(filteredDistVec, key=lambda item:item['dist'])

                    # compute the category listWeights
                    nextWordIdx = [word['word'] for word in filteredDistVec].index(nextWord)

                    # not sure about this part
                    idxs = []
                    for idx,word in enumerate(filteredDistVec):
                        if filteredDistVec[nextWordIdx]['dist'] == word['dist']:
                            idxs.append(idx)

                    listWeights[feature].append(1 - (sum(idxs)/len(idxs) / len(filteredDistVec)))

                pastWords.append(currentWord)

        for feature in listWeights:
            listWeights[feature] = np.mean(listWeights[feature])

        return [listWeights[key] for key in listWeights]

    # given a stimulus list and recalled words, compute the weights
    def get_fingerprint(pres_list, rec_list, feature_list, dist_funcs):
        distances = compute_distances(pres_list, feature_list, dist_funcs)
        return compute_feature_weights(pres_list, rec_list, feature_list, distances)

    # compute fingerprint for each list within a chunk
    fingerprint_matrix = [get_fingerprint(list(p), list(r), list(f), dist_funcs) for p, r, f in zip(pres_slice.as_matrix(), rec_slice.as_matrix(), feature_slice.as_matrix())]

    # return average over rows
    return np.mean(fingerprint_matrix, axis=0)

# THESE FUNCTIONS WILL BE DEPRECATED
def spc(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List'):
    return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=spc_helper, analysis_type='spc')

def pfr(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List'):
    return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=pfr_helper, analysis_type='pfr')

def lagcrp(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List'):
    return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=lagcrp_helper, analysis_type='lagcrp')

def fingerprint(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List'):
    return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=fingerprint_helper, analysis_type='fingerprint', pass_features=True)

# THIS FUNCTION REPLACES THE ANALYSIS FUNCTIONS ABOVE
def analyze(data, subjgroup=None, listgroup=None, subjname='Subject', listname='List', analysis=None):
    '''
    Analysis wrapper function
    '''

    if analysis is None:
        raise ValueError('You must pass an analysis type.')
    if analysis is 'accuracy':
        return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=accuracy_helper, analysis_type='accuracy')
    if analysis is 'spc':
        return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=spc_helper, analysis_type='spc')
    elif analysis is 'pfr':
        return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=pfr_helper, analysis_type='pfr')
    elif analysis is 'lagcrp':
        return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=lagcrp_helper, analysis_type='lagcrp')
    elif analysis is 'fingerprint':
        return analyze_chunk(data, subjgroup=subjgroup, listgroup=listgroup, subjname=subjname, listname=listname, analysis=fingerprint_helper, analysis_type='fingerprint', pass_features=True)
