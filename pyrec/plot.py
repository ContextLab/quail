from __future__ import division
import numpy as np
import pandas as pd
from .helpers import *

def plot(data, subjgroup=None, subjname='Subject', listgroup=None, listname='List'):
    """
    General plot function that groups data by subject/list number and performs analysis.

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

    #plot!
