#!/usr/bin/env python

from __future__ import division
import pandas as pd
import numpy as np

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
    listindex = [idx for idx,lst in enumerate(all_data[0])] if not listindex else listindex
    subjindex = [idx for idx,subj in enumerate(all_data)] if not subjindex else subjindex

    def make_multi_index(listindex, sub_num):
        return pd.MultiIndex.from_tuples([(sub_num,lst) for lst in listindex], names = ['Subject', 'List'])

    listindex = list(listindex)
    subjindex = list(subjindex)

    subs_list_of_dfs = [pd.DataFrame(sub_data, index=make_multi_index(listindex, subjindex[sub_num])) for sub_num,sub_data in enumerate(all_data)]

    return pd.concat(subs_list_of_dfs)

def format2tidy(df, subjname, listname, subjgroup, analysis_type=None):
    melted_df = pd.melt(df.T)
    melted_df[subjname]=""
    for idx,sub in enumerate(melted_df['Subject'].unique()):
        melted_df.loc[melted_df['Subject']==sub,subjname]=subjgroup[idx]
    if analysis_type in ['spc']:
        base = list(df.columns)
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = ['Subject', listname, 'Proportion Recalled', subjname, 'Position']
    elif analysis_type in ['pfr']:
        base = list(df.columns)
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = ['Subject', listname, 'Probability of First Recall', subjname, 'Position']
    elif analysis_type is 'lagcrp':
        base = range(int(-len(df.columns.values)/2),0)+[0]+range(1,int(len(df.columns.values)/2)+1)
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = ['Subject', listname, 'Conditional Response Probability', subjname, 'Position']
    elif analysis_type is 'fingerprint':
        base = list(df.columns.values)
        melted_df['Feature'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = ['Subject', listname, 'Clustering Score', subjname, 'Feature']
    elif analysis_type is 'accuracy':
        melted_df.columns = ['Subject', listname, 'Accuracy', subjname]

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

        for key in feature_example:
            if key in dist_funcs:
                pass
            elif type(feature_example[key]) is str:
                dist_funcs[key] = lambda a, b: int(a!=b)
            elif isinstance(feature_example[key], (int, long, float)) or all([isinstance(i, (int, long, float)) for i in feature_example[key]]):
                dist_funcs[key] = lambda a, b: np.linalg.norm(np.subtract(a,b))

        return dist_funcs

def stack_eggs(eggs):
    '''
    Takes a list of eggs, stacks them and reindexes the subject number

    Parameters
    ----------
    eggs : list of Egg data objects
        A list of Eggs that you want to combine


    Returns
    ----------
    new_egg : Egg data object
        A mega egg comprised of the input eggs stacked together

    '''
    from .egg import Egg

    pres = [egg.pres.loc[sub,:].values.tolist() for egg in eggs for sub in egg.pres.index.levels[0].values.tolist()]
    rec = [egg.rec.loc[sub,:].values.tolist()  for egg in eggs for sub in egg.rec.index.levels[0].values.tolist()]

    all_have_features = any([egg.features is not None for egg in eggs])

    if all_have_features:
        features = [egg.features.loc[sub,:].values.tolist() for egg in eggs for sub in egg.features.index.levels[0].values.tolist()]
        new_egg = Egg(pres=pres, rec=rec, features=features)
    else:
        new_egg = Egg(pres=pres, rec=rec)

    return new_egg
