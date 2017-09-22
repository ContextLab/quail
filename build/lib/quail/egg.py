#!/usr/bin/env python

import pandas as pd
from .analysis import recall_matrix
from .helpers import list2pd
from .helpers import default_dist_funcs
from .helpers import crack_egg
from .helpers import fill_missing
import pickle
import time

class Egg(object):
    """
    Data object for the quail package

    An Egg data object contains the data you need to analyze free recall experiments.
    This can be a single subject's data, or a group of subjects.  An Egg is comprised of
    a number of fields: the pres field contains the words/stimuli presented to the subject.
    The rec field contains the words/stimuli recalled by the subject. The feature field
    is optional, but may contain a dictionary of features for each stimulus.  This
    field is necessary to run the fingerprint analyses. Related to the features
    is the dist_funcs dictionary (also optional).  This dictionary specifies
    a set of distance functions required for the fingerprint analyses.  Finally,
    the meta field is an optional dictionary that contains any details useful for
    identifying the egg object

    Parameters
    ----------

    pres : list (subjects) of lists (study lists) of lists (words) of strings
        This is a nested list containing the presented words.  Internally, it will
        be converted into a multi-index Pandas DataFrame. Each row represents
        the presented words for a given list and each column represents a list.
        The cells should be lowercase words. The index will be a multi-index,
        where the first level reprensents the subject number and the second level
        represents the list number.

    rec : list (subjects) of lists (study lists) of lists (words) of strings
        This is a nested list containing the presented words.  Internally, it will
        be converted into a multi-index Pandas DataFrame. Each row represents
        the recalled words for a given list and each column represents a list.
        Each row represents the recalled words for a given list and each column
        represents a list. The cells should be lowercase words. The index will
        be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number

    features : list (subjects) of lists (study lists) of lists (words) of strings
        This is a nested list containing the presented words.  Internally, it will
        be converted into a multi-index Pandas DataFrame. Each row represents the
        presented words for a given list and each column represents a list. The
        cells should be a dictionary of features, where the keys are the name of
        the features, and the values are the feature values. The index will be a
        multi-index, where the first level represents the subject number and the
        second level represents the list number.

    dist_funcs : dict (optional)
        A dictionary of custom distance functions for stimulus features.  Each key should be the name of a feature
        and each value should be an inline distance function (e.g. `dist_funcs['feature_n'] = lambda a, b: abs(a-b)`)

    meta : dict (optional)
        Meta data about the study (i.e. version, description, date, etc.) can be saved here.

    subjgroup : list of strings or ints (optional)
        String/int variables indicating how to group over subjects.  Must be
        the length of the number of subjects

    subjname : string (optional)
        Name of the subject grouping variable. Default is 'Subject'.

    listgroup : list of strings or ints (optional)
        String/int variables indicating how to group over list.  Must be
        the length of the number of lists

    listname : string (optional)
        Name of the list grouping variable. Default is 'List'.

    Attributes
    ----------

    n_subjects : int
        Number of subjects in the egg object

    n_lists : int
        Number of lists per subject

    list_length : int
        Number of words in the lists

    date_created : time
        A timestamp when the egg was created

    """

    def __init__(self, pres=[[[]]], rec=[[[]]], features=None, dist_funcs=dict(),
                 meta={}, subjgroup=None, subjname='Subject', listgroup=None, listname='List'):

        if not all(isinstance(item, list) for sub in pres for item in sub):
            pres = [pres]

        if not all(isinstance(item, list) for sub in rec for item in sub):
            rec = [rec]

        if features is not None:
            if not all(isinstance(item, list) for sub in features for item in sub):
                features = [features]

        # make sure each subject has same number of lists
        pres = fill_missing(pres)
        rec = fill_missing(rec)

        self.pres = list2pd(pres)
        self.rec = list2pd(rec)
        self.meta = meta

        # attach features and dist funcs if they are passed
        if features:
            features = fill_missing(features)
            self.features = list2pd(features)
            self.dist_funcs = default_dist_funcs(dist_funcs, features[0][0][0])
        else:
            self.features = None
            self.dist_funcs = None

        # attach listgroup and subjgroup
        self.subjgroup=subjgroup
        self.subjname=subjname
        self.listgroup=listgroup
        self.listname=listname

        # attach attributes
        self.n_subjects = len(self.pres.index.levels[0].values)
        self.n_lists = len(self.pres.index.levels[1].values)
        self.list_length = len(self.pres.columns)
        self.date_created = time.strftime("%c")

        # attach methods
        self.crack = self.crack
        self.save = self.save
        self.info = self.info

    def info(self):
        """
        Print info about the data egg
        """
        print('Number of subjects: ' + str(self.n_subjects))
        print('Number of lists per subject: ' + str(self.n_lists))
        print('Number of words per list: ' + str(self.list_length))
        print('Date created: ' + str(self.date_created))
        print('Meta data: ' + str(self.meta))

    def save(self, filepath):
        """
        Save a pickled egg
        """

        with open(filepath + '.egg', 'wb') as f:
            pickle.dump(self, f)
            print('pickle saved.')

    def crack(self, subjects=None, lists=None):
        """
        Wraps crack_egg function to take an egg and returns a subset of the subjects

        Parameters
        ----------
        subjects : list
            List of subject idxs

        lists : list
            List of lists idxs

        Returns
        ----------
        new_egg : Egg data object
            A mega egg comprised of the input eggs stacked together
        """
        return crack_egg(self, subjects, lists)
