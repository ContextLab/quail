#!/usr/bin/env python

from __future__ import division
from builtins import str
from builtins import range
import pandas as pd
import numpy as np
import pickle
import six

def list2pd(all_data, subjindex=None, listindex=None):
    """
    Makes multi-indexed dataframe of subject data

    Parameters
    ----------
    all_data : list of lists of strings
        strings are either all presented or all recalled items, in the order of presentation or recall
        *should also work for presented / recalled ints and floats, if desired


    Returns
    ----------
    subs_list_of_dfs : multi-indexed dataframe
        dataframe of subject data (presented or recalled words/items), indexed by subject and list number
        cell populated by the term presented or recalled in the position indicated by the column number

    """
    # set default index if it is not defined
    # max_nlists = max(map(lambda x: len(x), all_data))
    listindex = [[idx for idx in range(len(sub))] for sub in all_data] if not listindex else listindex
    subjindex = [idx for idx,subj in enumerate(all_data)] if not subjindex else subjindex


    def make_multi_index(listindex, sub_num):
        return pd.MultiIndex.from_tuples([(sub_num,lst) for lst in listindex], names = ['Subject', 'List'])

    listindex = list(listindex)
    subjindex = list(subjindex)

    subs_list_of_dfs = [pd.DataFrame(sub_data, index=make_multi_index(listindex[sub_num], subjindex[sub_num])) for sub_num,sub_data in enumerate(all_data)]

    return pd.concat(subs_list_of_dfs)

def format2tidy(df, subjname, listname, subjgroup, analysis=None, position=0):
    melted_df = pd.melt(df.T)
    melted_df[subjname]=""
    for idx,sub in enumerate(melted_df['Subject'].unique()):
        melted_df.loc[melted_df['Subject']==sub,subjname]=subjgroup[idx]
    if analysis=='spc':
        base = list(df.columns)
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = ['Subject', listname, 'Proportion Recalled', subjname, 'Position']
    elif analysis in ['pfr', 'pnr']:
        base = list(df.columns)
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = ['Subject', listname, 'Probability of Recall: Position ' + str(position), subjname, 'Position']
    elif analysis=='lagcrp':
        base = list(range(int(-len(df.columns.values)/2),int(len(df.columns.values)/2)+1))
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = ['Subject', listname, 'Conditional Response Probability', subjname, 'Position']
    elif analysis=='fingerprint' or analysis=='fingerprint_temporal':
        base = list(df.columns.values)
        melted_df['Feature'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = ['Subject', listname, 'Clustering Score', subjname, 'Feature']
    elif analysis=='accuracy':
        melted_df.columns = ['Subject', listname, 'Accuracy', subjname]
    elif analysis=='temporal':
        melted_df.columns = ['Subject', listname, 'Temporal Clustering Score', subjname]
    return melted_df

def recmat2egg(recmat, list_length=None):
        """
        Creates egg data object from zero-indexed recall matrix

        Parameters
        ----------
        recmat : list of lists (subs) of lists (encoding lists) of ints or 2D numpy array
            recall matrix representing serial positions of freely recalled words \
            e.g. [[[16, 15, 0, 2, 3, None, None...], [16, 4, 5, 6, 1, None, None...]]]

        list_length : int
            The length of each list (e.g. 16)


        Returns
        ----------
        egg : Egg data object
            egg data object computed from the recall matrix
        """
        from .egg import Egg as Egg

        pres = [[[str(word) for word in list(range(0,list_length))] for reclist in recsub] for recsub in recmat]
        rec = [[[str(word) for word in reclist if word is not None] for reclist in recsub] for recsub in recmat]

        return Egg(pres=pres,rec=rec)

def default_dist_funcs(dist_funcs, feature_example):
        """
        Fills in default distance metrics for fingerprint analyses
        """

        if dist_funcs is None:
            dist_funcs = dict()

        for key in feature_example:
            if key in dist_funcs:
                pass
            if key == 'item':
                pass
            elif isinstance(feature_example[key], (six.string_types, six.binary_type)):
                dist_funcs[key] = 'match'
            elif isinstance(feature_example[key], (int, np.integer, float)) or all([isinstance(i, (int, np.integer, float)) for i in feature_example[key]]):
                dist_funcs[key] = 'euclidean'

        return dist_funcs

def stack_eggs(eggs, meta='concatenate'):
    '''
    Takes a list of eggs, stacks them and reindexes the subject number

    Parameters
    ----------
    eggs : list of Egg data objects
        A list of Eggs that you want to combine
    meta : string
        Determines how the meta data of each Egg combines. Default is 'concatenate'
        'concatenate' concatenates keys in meta data dictionary shared between eggs, and copies non-overlapping keys
        'separate' keeps the Eggs' meta data dictionaries separate, with each as a list index in the stacked meta data


    Returns
    ----------
    new_egg : Egg data object
        A mega egg comprised of the input eggs stacked together

    '''
    from .egg import Egg

    pres = [egg.pres.loc[sub,:].values.tolist() for egg in eggs for sub in egg.pres.index.levels[0].values.tolist()]
    rec = [egg.rec.loc[sub,:].values.tolist() for egg in eggs for sub in egg.rec.index.levels[0].values.tolist()]

    if meta is 'concatenate':
        new_meta = {}
        for egg in eggs:
            for key in egg.meta:
                if key in new_meta:
                    new_meta[key] = list(new_meta[key])
                    new_meta[key].extend(egg.meta.get(key))
                else:
                    new_meta[key] = egg.meta.get(key)

    elif meta is 'separate':
        new_meta = list(egg.meta for egg in eggs)

    return Egg(pres=pres, rec=rec, meta=new_meta)

def crack_egg(egg, subjects=None, lists=None):
    '''
    Takes an egg and returns a subset of the subjects or lists

    Parameters
    ----------
    egg : Egg data object
        Egg that you want to crack

    subjects : list
        List of subject idxs

    lists : list
        List of lists idxs

    Returns
    ----------
    new_egg : Egg data object
        A sliced egg, good on a salad

    '''
    from .egg import Egg

    if hasattr(egg, 'features'):
        all_have_features = egg.features is not None
    else:
        all_have_features=False
    opts = {}

    if subjects is None:
        subjects = egg.pres.index.levels[0].values.tolist()
    elif type(subjects) is not list:
        subjects = [subjects]

    if lists is None:
        lists = egg.pres.index.levels[1].values.tolist()
    elif type(lists) is not list:
        lists = [lists]

    idx = pd.IndexSlice
    pres = egg.pres.loc[idx[subjects,lists],egg.pres.columns]
    rec = egg.rec.loc[idx[subjects,lists],egg.rec.columns]

    pres = [pres.loc[sub,:].values.tolist() for sub in subjects]
    rec = [rec.loc[sub,:].values.tolist() for sub in subjects]

    if all_have_features:
        features = egg.features.loc[idx[subjects,lists],egg.features.columns]
        opts['features'] = [features.loc[sub,:].values.tolist() for sub in subjects]

    return Egg(pres=pres, rec=rec, **opts)

def df2list(df):
    """
    Convert a MultiIndex df to list

    Parameters
    ----------

    df : pandas.DataFrame
        A MultiIndex DataFrame where the first level is subjects and the second
        level is lists (e.g. egg.pres)

    Returns
    ----------

    lst : a list of lists of lists of values
        The input df reformatted as a list

    """
    subjects = df.index.levels[0].values.tolist()
    lists = df.index.levels[1].values.tolist()
    idx = pd.IndexSlice
    df = df.loc[idx[subjects,lists],df.columns]
    lst = [df.loc[sub,:].values.tolist() for sub in subjects]
    return lst

def fill_missing(x):
    """
    Fills in missing lists (assumes end lists are missing)
    """

    # find subject with max number of lists
    maxlen = max([len(xi) for xi in x])

    subs = []

    for sub in x:
        if len(sub)<maxlen:
            for i in range(maxlen-len(sub)):
                sub.append([])
            new_sub = sub
        else:
            new_sub = sub
        subs.append(new_sub)
    return subs

def parse_egg(egg):
    """Parses an egg and returns fields"""
    pres_list = egg.get_pres_items().values[0]
    rec_list = egg.get_rec_items().values[0]
    feature_list = egg.get_pres_features().values[0]
    dist_funcs = egg.dist_funcs
    return pres_list, rec_list, feature_list, dist_funcs

def merge_pres_feats(pres, features):
    """
    Helper function to merge pres and features to support legacy features argument
    """

    sub = []
    for psub, fsub in zip(pres, features):
        exp = []
        for pexp, fexp in zip(psub, fsub):
            lst = []
            for p, f in zip(pexp, fexp):
                p.update(f)
                lst.append(p)
            exp.append(lst)
        sub.append(exp)
    return sub

def check_nan(x):
    y = pd.isnull(x)
    if type(y) is bool:
        return y
    else:
        return False

def r2z(r):
    """
    Function that calculates the Fisher z-transformation

    Parameters
    ----------
    r : int or ndarray
        Correlation value

    Returns
    ----------
    result : int or ndarray
        Fishers z transformed correlation value


    """
    with np.errstate(invalid='ignore', divide='ignore'):
        return 0.5 * (np.log(1 + r) - np.log(1 - r))

def z2r(z):
    """
    Function that calculates the inverse Fisher z-transformation

    Parameters
    ----------
    z : int or ndarray
        Fishers z transformed correlation value

    Returns
    ----------
    result : int or ndarray
        Correlation value


    """
    with np.errstate(invalid='ignore', divide='ignore'):
        return (np.exp(2 * z) - 1) / (np.exp(2 * z) + 1)

def _format(p, r):
    p = np.matrix([np.array(i) for i in p])
    if p.shape[0]==1:
        p=p.T
    r = map(lambda x: [np.nan]*p.shape[1] if check_nan(x) else x, r)
    r = np.matrix([np.array(i) for i in r])
    if r.shape[0]==1:
        r=r.T
    return p, r

def shuffle_egg(egg):
    """ Shuffle an Egg's recalls"""
    from .egg import Egg
    pres, rec, features, dist_funcs = parse_egg(egg)

    if pres.ndim==1:
        pres = pres.reshape(1, pres.shape[0])
        rec = rec.reshape(1, rec.shape[0])
        features = features.reshape(1, features.shape[0])

    for ilist in range(rec.shape[0]):
        idx = np.random.permutation(rec.shape[1])
        rec[ilist,:] = rec[ilist,idx]

    return Egg(pres=pres, rec=rec, features=features, dist_funcs=dist_funcs)
