#!/usr/bin/env python

import pandas as pd
from .analysis import recall_matrix
from .helpers import list2pd
from .helpers import default_dist_funcs

class Pyro(object):
    """
    Data object for the pyrec package

    This class contains free recall data and metadata that will be used by pyrec

    Attributes
    ----------

    pres : pd.DataFrame
        Dataframe containing the presented words.  Each row represents the presented words for a given list and each column
        represents a list. The cells should be lowercase words. The index will be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number

    rec : pd.DataFrame
        Dataframe containing the words recalled.  Each row represents the recalled words for a given list and each column
        represents a list.  Each row represents the recalled words for a given list and each column
        represents a list. The cells should be lowercase words. The index will be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number

    features : pd.DataFrame (optional)
        Dataframe containing the features for presented words.  Each row represents the presented words for a given list and each column
        represents a list. The cells should be a dictionary of features, where the keys are the name of the features, and the values are the feature values.
        The index will be a multi-index, where the first level reprensents the subject number and the second level represents the list number

    dist_funcs : dict (optional)
        A dictionary of custom distance functions for stimulus features.  Each key should be the name of a feature
        and each value should be an inline distance function (e.g. `dist_funcs['feature_n'] = lambda a, b: abs(a-b)`)

    meta : dict (optional)
        Meta data about the study (i.e. version, description, date, etc.) can be saved here.

    """


    def __init__(self, pres=[[[]]], rec=[[[]]], features=[[[]]], dist_funcs=dict(), meta={}):

        self.pres = list2pd(pres)
        self.rec = list2pd(rec)
        self.meta = meta

        # attach features and dist funcs if they are passed
        if features != [[[]]]:
            self.features = list2pd(features)
            self.dist_funcs = default_dist_funcs(dist_funcs, features[0][0][0])
        else:
            self.features = None
            self.dist_funcs = None
