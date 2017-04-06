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

def format2tidy(df, subjname, listname, analysis_type=None):
    melted_df = pd.melt(df.T)
    if analysis_type in ['spc']:
        base = list(df.columns)
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = [subjname, listname, 'Proportion Recalled', 'Position']
    elif analysis_type in ['pfr']:
        base = list(df.columns)
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = [subjname, listname, 'Probability of First Recall', 'Position']
    elif analysis_type is 'lagcrp':
        base = range(int(-len(df.columns.values)/2),0)+[0]+range(1,int(len(df.columns.values)/2)+1)
        melted_df['Position'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = [subjname, listname, 'Conditional Response Probability', 'Position']
    elif analysis_type is 'fingerprint':
        base = list(df.columns.values)
        melted_df['Feature'] = base * int(melted_df.shape[0] / len(base))
        melted_df.columns = [subjname, listname, 'Clustering Score', 'Feature']
    elif analysis_type is 'accuracy':
        base = list(df.columns.values)
        melted_df.columns = [subjname, listname, 'Accuracy']

    return melted_df

def recmat2pyro(recmat):
        """
        Creates pyro data object from zero-indexed recall matrix

        Parameters
        ----------
        recmat : list of lists (subs) of lists (encoding lists) of ints or 2D numpy array
            recall matrix representing serial positions of freely recalled words \
            e.g. [[[16, 15, 1, 2, 3, None, None...], [16, 4, 5, 6, 1, None, None...]]]


        Returns
        ----------
        pyro : Pyro data object
            pyro data object computed from the recall matrix
        """
        from .pyro import Pyro as Pyro

        pres = [[[str(word) for word in list(range(0,len(reclist)))] for reclist in recsub] for recsub in recmat]
        rec = [[[str(word) for word in reclist if word is not None] for reclist in recsub] for recsub in recmat]

        return Pyro(pres=pres,rec=rec)

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
