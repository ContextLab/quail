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
from .clustering import fingerprint_helper

analyses = {
    'accuracy' : accuracy_helper,
    'spc' : spc_helper,
    'pfr' : pnr_helper,
    'pnr' : pnr_helper,
    'lagcrp' : lagcrp_helper,
    'fingerprint' : fingerprint_helper,
    'temporal' : fingerprint_helper
}

# main analysis function
def analyze(egg, subjgroup=None, listgroup=None, subjname='Subject',
            listname='List', analysis=None, position=0, permute=False,
            n_perms=1000, parallel=False, match='exact',
            distance='euclidean', features=None, ts=None):
    """
    General analysis function that groups data by subject/list number and performs analysis.

    Parameters
    ----------
    egg : Egg data object
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

    match : str (exact, best or smooth)
        Matching approach to compute recall matrix.  If exact, the presented and
        recalled items must be identical (default).  If best, the recalled item
        that is most similar to the presented items will be selected. If smooth,
        a weighted average of all presented items will be used, where the
        weights are derived from the similarity between the recalled item and
        each presented item.

    distance : str
        The distance function used to compare presented and recalled items.
        Applies only to 'best' and 'smooth' matching approaches.  Can be any
        distance function supported by numpy.spatial.distance.cdist.


    Returns
    ----------
    result : quail.FriedEgg
        Class instance containing the analysis results

    """
    if analysis is None:
        raise ValueError('You must pass an analysis type.')

    if analysis not in analyses.keys():
        raise ValueError('Analysis not recognized. Choose one of the following: '
                        'accuracy, spc, pfr, lag-crp, fingerprint, temporal')

    from ..egg import FriedEgg

    if hasattr(egg, 'subjgroup'):
        if egg.subjgroup is not None:
            subjgroup = egg.subjgroup

    if hasattr(egg, 'subjname'):
        if egg.subjname is not None:
            subjname = egg.subjname

    if hasattr(egg, 'listgroup'):
        if egg.listgroup is not None:
            listgroup = egg.listgroup

    if hasattr(egg, 'listname'):
        if egg.listname is not None:
            listname = egg.listname

    if features is None:
        features = egg.feature_names

    opts = {
        'subjgroup' : subjgroup,
        'listgroup' : listgroup,
        'subjname' : subjname,
        'parallel' : parallel,
        'match' : match,
        'distance' : distance,
        'features' : features,
        'analysis_type' : analysis,
        'analysis' : analyses[analysis]
    }

    if analysis is 'pfr':
        opts.update({'position' : 0})
    elif analysis is 'pnr':
        opts.update({'position' : position})
    if analysis is 'temporal':
        opts.update({'features' : ['temporal']})
    if analysis in ['temporal', 'fingerprint']:
        opts.update({'permute' : permute, 'n_perms' : n_perms})
    if analysis is 'lagcrp':
        opts.update({'ts' : ts})

    return FriedEgg(data=_analyze_chunk(egg, **opts), analysis=analysis,
                    list_length=egg.list_length, n_lists=egg.n_lists,
                    n_subjects=egg.n_subjects, position=position)

def _analyze_chunk(data, subjgroup=None, subjname='Subject', listgroup=None,
                   listname='List', analysis=None, analysis_type=None,
                   pass_features=False, features=None, parallel=False,
                   **kwargs):
    """
    Private function that groups data by subject/list number and performs
    analysis for a chunk of data.

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
        Logical indicating whether the analyses uses the features field of the
        Egg

    Returns
    ----------
    analyzed_data : Pandas DataFrame
        DataFrame containing the analysis results

    """

    # perform the analysis
    def _analysis(c):
        subj, lst = c
        subjects = [s for s in subjdict[subj]]
        lists = [l for l in listdict[subj][lst]]
        s = data.crack(lists=lists, subjects=subjects)
        index = pd.MultiIndex.from_arrays([[subj],[lst]], names=[subjname, listname])
        opts = dict()
        if analysis_type is 'fingerprint':
                opts.update({'columns' : features})
        elif analysis_type is 'lagcrp':
            if kwargs['ts']:
                opts.update({'columns' : range(-kwargs['ts'],kwargs['ts']+1)})
            else:
                opts.update({'columns' : range(-data.list_length,data.list_length+1)})
        return pd.DataFrame([analysis(s, features=features, **kwargs)],
                            index=index, **opts)

    subjgroup = subjgroup if subjgroup else data.pres.index.levels[0].values
    listgroup = listgroup if listgroup else data.pres.index.levels[1].values

    subjdict = {subj : data.pres.index.levels[0].values[subj==np.array(subjgroup)] for subj in set(subjgroup)}

    if all(isinstance(el, list) for el in listgroup):
        listdict = [{lst : data.pres.index.levels[1].values[lst==np.array(listgrpsub)] for lst in set(listgrpsub)} for listgrpsub in listgroup]
    else:
        listdict = [{lst : data.pres.index.levels[1].values[lst==np.array(listgroup)] for lst in set(listgroup)} for subj in subjdict]

    chunks = [(subj, lst) for subj in subjdict for lst in listdict[0]]

    if parallel:
        import multiprocessing
        from pathos.multiprocessing import ProcessingPool as Pool
        p = Pool(multiprocessing.cpu_count())
        res = p.map(_analysis, chunks)
    else:
        res = [_analysis(c) for c in chunks]

    return pd.concat(res)
