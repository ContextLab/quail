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

def multi2tidy(df):
    melted_df = pd.melt(df.T)
    if df.type in ['spc','pfr','plr']
        base = list(df.columns)
    elif df.type is 'lag_crp':
        # change this to reflect lag_crp x
        base = list(df.columns)
    melted_df['position'] = base * (melted_df.shape[0] / len(base))
    return melted_df
