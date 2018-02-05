#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from builtins import zip
from builtins import range
import six
import numpy as np
import pandas as pd
import warnings
import six
from ..helpers import *
from ..distance import dist_funcs as dist_funcs_dict
from .recmat import recall_matrix
from .accuracy import accuracy_helper
from .spc import spc_helper
from .pnr import pnr_helper
from .lagcrp import lagcrp_helper
from .temporal import temporal_helper
from .fingerprint import fingerprint_helper, fingerprint_temporal_helper

# main analysis function
def analyze(data, subjgroup=None, listgroup=None, subjname='Subject',
            listname='List', analysis=None, position=0, permute=False, n_perms=1000,
            parallel=False, match='exact', distance='correlation'):
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
        temporal or fingerprint

    position : int
        Optional argument for pnr analysis.  Defines encoding position of item
        to run pnr.  Default is 0, and it is zero indexed

    permute : bool
        Optional argument for fingerprint/temporal cluster analyses. Determines
        whether to correct clustering scores by shuffling recall order for each list
        to create a distribution of clustering scores (for each feature). The
        "corrected" clustering score is the proportion of clustering scores in
        that random distribution that were lower than the clustering score for
        the observed recall sequence. Default is False.

    n_perms : int
        Optional argument for fingerprint/temporal cluster analyses. Number of
        permutations to run for "corrected" clustering scores. Default is 1000 (
        per recall list).

    parallel : bool
        Option to use multiprocessing (this can help speed up the permutations
        tests in the clustering calculations)

    Returns
    ----------
    analyzed_data : Pandas DataFrame
        DataFrame containing the analysis results

    """

    from ..egg import FriedEgg

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

    if analysis is 'accuracy':
        r = _analyze_chunk(data, subjgroup=subjgroup,
                          listgroup=listgroup,
                          subjname=subjname,
                          listname=listname,
                          analysis=accuracy_helper,
                          analysis_type='accuracy',
                          pass_features=False,
                          parallel=parallel,
                          match=match,
                          distance=distance)
    elif analysis is 'spc':
        r = _analyze_chunk(data, subjgroup=subjgroup,
                          listgroup=listgroup,
                          subjname=subjname,
                          listname=listname,
                          analysis=spc_helper,
                          analysis_type='spc',
                          pass_features=False,
                          parallel=parallel,
                          match=match,
                          distance=distance)
    elif analysis is 'pfr':
        r = _analyze_chunk(data, subjgroup=subjgroup,
                          listgroup=listgroup,
                          subjname=subjname,
                          listname=listname,
                          analysis=pnr_helper,
                          analysis_type='pfr',
                          pass_features=False,
                          position=0,
                          parallel=parallel,
                          match=match,
                          distance=distance)
    elif analysis is 'pnr':
        r = _analyze_chunk(data, subjgroup=subjgroup,
                          listgroup=listgroup,
                          subjname=subjname,
                          listname=listname,
                          analysis=pnr_helper,
                          analysis_type='pnr',
                          pass_features=False,
                          position=position,
                          parallel=parallel,
                          match=match,
                          distance=distance)
    elif analysis is 'lagcrp':
        r = _analyze_chunk(data, subjgroup=subjgroup,
                          listgroup=listgroup,
                          subjname=subjname,
                          listname=listname,
                          analysis=lagcrp_helper,
                          analysis_type='lagcrp',
                          pass_features=False,
                          parallel=parallel)
        # set indices for lagcrp
        r.columns=range(-int((len(r.columns)-1)/2),int((len(r.columns)-1)/2)+1)
    elif analysis is 'fingerprint':
        r = _analyze_chunk(data, subjgroup=subjgroup,
                          listgroup=listgroup,
                          subjname=subjname,
                          listname=listname,
                          analysis=fingerprint_helper,
                          analysis_type='fingerprint',
                          pass_features=True,
                          permute=permute,
                          n_perms=n_perms,
                          parallel=parallel)
    elif analysis is 'temporal':
        r = _analyze_chunk(data, subjgroup=subjgroup,
                          listgroup=listgroup,
                          subjname=subjname,
                          listname=listname,
                          analysis=temporal_helper,
                          analysis_type='temporal',
                          permute=permute,
                          n_perms=n_perms,
                          parallel=parallel)
    elif analysis is 'fingerprint_temporal':
        r = _analyze_chunk(data, subjgroup=subjgroup,
                          listgroup=listgroup,
                          subjname=subjname,
                          listname=listname,
                          analysis=fingerprint_temporal_helper,
                          analysis_type='fingerprint_temporal',
                          pass_features=True,
                          permute=permute,
                          n_perms=n_perms,
                          parallel=parallel)
    else:
        raise ValueError('Analysis not recognized. Choose one of the following: '
                         'accuracy, spc, pfr, lag-crp, fingerprint, temporal, '
                         'fingerprint_temporal')

    # return analysis result
    return FriedEgg(data=r, analysis=analysis, list_length=data.list_length,
                    n_lists=data.n_lists, n_subjects=data.n_subjects,
                    position=position)

def _analyze_chunk(data, subjgroup=None, subjname='Subject', listgroup=None, listname='List', analysis=None, analysis_type=None, pass_features=False, **kwargs):
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

    # perform the analysis
    def perform_analysis(subj, lst):

        # get data slice for presentation and recall
        pres_slice = data.pres.loc[[(s,l) for s in subjdict[subj] for l in listdict[subj][lst] if all(~pd.isnull(data.pres.loc[(s,l)]))]]
        pres_slice = pres_slice.applymap(lambda x: x['item'])
        pres_slice.list_length = data.list_length

        rec_slice = data.rec.loc[[(s,l) for s in subjdict[subj] for l in listdict[subj][lst] if all(~pd.isnull(data.pres.loc[(s,l)]))]]
        rec_slice = rec_slice.applymap(lambda x: x['item'] if x is not None else np.nan)

        # if features are need for analysis, get the features for this slice of data
        if pass_features:
            feature_slice = data.pres.loc[[(s,l) for s in subjdict[subj] for l in listdict[subj][lst] if all(~pd.isnull(data.pres.loc[(s,l)]))]]
            feature_slice = feature_slice.applymap(lambda x: {k:v for k,v in x.items() if k != 'item'})

        # generate indices
        index = pd.MultiIndex.from_arrays([[subj],[lst]], names=[subjname, listname])

        # perform analysis for each data chunk
        if pass_features:
            return pd.DataFrame([analysis(pres_slice, rec_slice, feature_slice, data.dist_funcs, **kwargs)], index=index, columns=[feature for feature in list(feature_slice[0].as_matrix()[0].keys())])
        else:
            return pd.DataFrame([analysis(pres_slice, rec_slice, **kwargs)], index=index)


    # if no grouping, set default to iterate over each list independently
    subjgroup = subjgroup if subjgroup else data.pres.index.levels[0].values
    listgroup = listgroup if listgroup else data.pres.index.levels[1].values

    # create a dictionary for grouping
    subjdict = {subj : data.pres.index.levels[0].values[subj==np.array(subjgroup)] for subj in set(subjgroup)}

    # allow for lists of listgroup arguments
    if all(isinstance(el, list) for el in listgroup):
        listdict = [{lst : data.pres.index.levels[1].values[lst==np.array(listgrpsub)] for lst in set(listgrpsub)} for listgrpsub in listgroup]
    else:
        listdict = [{lst : data.pres.index.levels[1].values[lst==np.array(listgroup)] for lst in set(listgroup)} for subj in subjdict]

    # create list of chunks to process
    a=[]
    b=[]
    for subj in subjdict:
        for lst in listdict[0]:
            a.append(subj)
            b.append(lst)

    # handle parellel kwarg
    parallel=kwargs['parallel']
    del kwargs['parallel']

    # if we're running permutation tests, use multiprocessing
    if parallel:
        import multiprocessing
        from pathos.multiprocessing import ProcessingPool as Pool
        p = Pool(multiprocessing.cpu_count())
        analyzed_data = p.map(perform_analysis, a, b)
    else:
        analyzed_data = [perform_analysis(ai, bi) for ai, bi in zip(a, b)]

    # concatenate slices
    return pd.concat(analyzed_data)
