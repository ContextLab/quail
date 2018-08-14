#!/usr/bin/env python
from __future__ import print_function
from builtins import str
from builtins import object
import pickle
import time
import deepdish as dd
import inspect
import warnings
import pandas as pd
import numpy as np
from .analysis.recmat import recall_matrix
from .analysis.analysis import analyze
from .plot import plot
from .helpers import list2pd, default_dist_funcs, crack_egg, fill_missing, merge_pres_feats, df2list

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

    pres : list (subjects) of lists (experiment) of lists (list/block) of strings or dictionaries.
        This is a nested list containing the presented stimuli/stimulus features.
        The outer list groups the data into subjects, the middle list groups the
        data into experiments and the inner list groups the data into stimuli
        presented together in one block (or list). Each item within the list can
        be a string representing the stimulus or a dictionary representing the
        stimuli and its features. If dictionaries are passed, identify the stimulus
        name using the 'item' key and a string label. To represent additional
        stimulus features, use any text (str) label as the key and a value of the
        following types: string, int, float, list, array.

    rec : list (subjects) of lists (experiment) of lists (list/block) of strings or dictionaries.
        This is a nested list containing the recalled stimuli/stimulus features.
        The outer list groups the data into subjects, the middle list groups the
        data into experiments and the inner list groups the data into stimuli
        presented together in one block (or list). Each item within the list can
        be a string representing the stimulus or a dictionary representing the
        stimuli and its features. If dictionaries are passed, identify the stimulus
        name using the 'item' key and a string label. To represent additional
        stimulus features, use any text (str) label as the key and a value of the
        following types: string, int, float, list, array.

    features : list (subjects) of lists (experiment) of lists (list/block) of strings or dictionaries.
        This is DEPRECATED, but left in for legacy support. This is a nested list
        containing the stimuli/stimulus features. The outer list groups the data
        into subjects, the middle list groups the data into experiments and the
        inner list groups the data into stimuli presented together in one block
        (or list). Each item within the list should be a dictionary representing
        stimulus features. Each dictionary should contain a text (str) label as
        the key and a value of the following types: string, int, float, list, array.

    dist_funcs : dict (optional)
        A dictionary of custom distance functions for stimulus features. Each
        key should be the name of a feature and each value should be a string
        representation of an inline distance function
        (e.g. `dist_funcs['feature_n'] = 'lambda a, b: abs(a-b)''`)

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

    recmat : list (subjects) of lists (experiment) of lists (list/block) of ints.
        An egg can be optionally created directly from recall matrices. A recall
        matrix specifies sequences by listing out there indices in the order they
        were recalled (e.g. [4, 2, 1, None, None]).

    list_length : int
        The length of the presented lists.  Used to create an egg from a recall
        matrix (optional).  If list_length is not passed, the length of the
        presented lists is assumed to be the length of the first list passed.

    Attributes
    ----------

    pres : Pandas.DataFrame
        A multi-index Pandas DataFrame representing the stimuli presented. The
        rows of the dataframe created represent distinct presentation blocks and
        the columns represent stimuli presented within a block. Each cell of the
        dataframe is a dictionary where the 'stimulus' key is a text label of
        the stimulus and any other text keys are features of the presented
        stimulus. The dataframe index will be a multi-index, where the first
        level represents the subject number and the second level represents the
        list (or presentation block) number.

    rec : Pandas.DataFrame
        A multi-index Pandas DataFrame representing the stimuli recalled. The
        rows of the dataframe created represent distinct presentation blocks and
        the columns represent stimuli presented within a block. Each cell of the
        dataframe is a dictionary where the 'stimulus' key is a text label of
        the stimulus and any other text keys are features of the presented
        stimulus. The dataframe index will be a multi-index, where the first
        level represents the subject number and the second level represents the
        list (or presentation block) number.

    n_subjects : int
        Number of subjects in the egg object

    n_lists : int
        Number of lists per subject

    list_length : int
        Number of words in the lists

    date_created : time
        A timestamp when the egg was created

    """

    def __init__(self, pres=None, rec=None, features=None, dist_funcs=None,
                 meta=None, subjgroup=None, subjname='Subject', listgroup=None,
                 listname='List', date_created=None, recmat=None,
                 list_length=None):

        # handle if recmat is passed
        if recmat is not None:
            if list_length is None:
                warnings.warn('Recall matrix passed, but list_length was not '
                              'defined. Inferring from length of first list')
                list_length = len(recmat[0][0])
            pres = [[[str(word) for word in list(range(0,list_length))] for reclist in recsub] for recsub in recmat]
            rec = [[[str(word) for word in reclist if word is not None] for reclist in recsub] for recsub in recmat]
        else:
            # check to see if pres is a list(list(list))
            if not all(isinstance(item, list) for sub in pres for item in sub):
                pres = [pres]

            # check to see if rec is a list(list(list))
            if not all(isinstance(item, list) for sub in rec for item in sub):
                rec = [rec]

        # make sure each subject has same number of lists
        pres = fill_missing(pres)
        rec = fill_missing(rec)

        # if pres is strings, reformat
        if type(pres[0][0][0]) is not dict:
            pres = [[[{'item' : x} for x in y] for y in z] for z in pres]

        # if pres is strings, reformat
        if type(rec[0][0][0]) is not dict:
            rec = [[[{'item' : x} for x in y] for y in z] for z in rec]

        # if item is missing from pres, add it
        if 'item' not in pres[0][0][0]:
            [[[x.update({'item' : i}) for i, x in enumerate(y)] for y in z] for z in pres]
        if 'temporal' not in pres[0][0][0]:
            [[[x.update({'temporal' : i}) for i, x in enumerate(y)] for y in z] for z in pres]

        # if item is missing from rec, add it
        if 'item' not in rec[0][0][0]:
            [[[x.update({'item' : i}) for i, x in enumerate(y)] for y in z] for z in rec]
        if 'temporal' not in rec[0][0][0]:
            [[[x.update({'temporal' : i}) for i, x in enumerate(y)] for y in z] for z in rec]

        # attach features and dist funcs if they are passed
        if features is not None:
            if not all(isinstance(item, list) for sub in features for item in sub):
                features = [features]
            features = fill_missing(features)
            pres = merge_pres_feats(pres, features)

        # add default dist funcs if some or all are not provided
        self.dist_funcs = default_dist_funcs(dist_funcs, pres[0][0][0])

        # attach the rest of the variables
        self.pres = list2pd(pres).applymap(lambda x: {'item' : np.nan} if pd.isnull(x) else x)
        self.feature_names = list(self.get_pres_features()[0][0][0])
        self.rec = list2pd(rec).applymap(lambda x: {'item' : np.nan} if pd.isnull(x) else x)
        self.subjgroup=subjgroup
        self.subjname=subjname
        self.listgroup=listgroup
        self.listname=listname
        self.n_subjects = len(self.pres.index.levels[0].values)
        self.n_lists = len(self.pres.index.levels[1].values)
        self.list_length = len(self.pres.columns)

        if meta is None:
            self.meta = {}
        else:
            self.meta = meta

        if date_created is None:
            self.date_created = time.strftime("%c")
        else:
            self.date_created = date_created

    def get_pres_items(self):
        """
        Returns a df of presented items
        """
        return self.pres.applymap(lambda x: x['item'])

    def get_pres_features(self, features=None):
        """
        Returns a df of features for presented items
        """
        if features is None:
            features = self.dist_funcs.keys()
        elif not isinstance(features, list):
            features = [features]
        return self.pres.applymap(lambda x: {k:v for k,v in x.items() if k in features} if x is not None else None)

    def get_rec_items(self):
        """
        Returns a df of recalled items
        """
        return self.rec.applymap(lambda x: x['item'] if x is not None else x)

    def get_rec_features(self, features=None):
        """
        Returns a df of features for recalled items
        """
        if features is None:
            features = self.dist_funcs.keys()
        elif not isinstance(features, list):
            features = [features]
        return self.rec.applymap(lambda x: {k:v for k,v in x.items() if k != 'item'} if x is not None else None)


    def info(self):
        """
        Print info about the data egg
        """
        print('Number of subjects: ' + str(self.n_subjects))
        print('Number of lists per subject: ' + str(self.n_lists))
        print('Number of words per list: ' + str(self.list_length))
        print('Date created: ' + str(self.date_created))
        print('Meta data: ' + str(self.meta))

    def save(self, fname, compression='blosc'):
        """
        Save method for the Egg object

        The data will be saved as a 'egg' file, which is a dictionary containing
        the elements of a Egg saved in the hd5 format using
        `deepdish`.

        Parameters
        ----------

        fname : str
            A name for the file.  If the file extension (.egg) is not specified,
            it will be appended.

        compression : str
            The kind of compression to use.  See the deepdish documentation for
            options: http://deepdish.readthedocs.io/en/latest/api_io.html#deepdish.io.save

        """

        # put egg vars into a dict
        egg = {
            'pres' : df2list(self.pres),
            'rec' : df2list(self.rec),
            'dist_funcs' : self.dist_funcs,
            'subjgroup' : self.subjgroup,
            'subjname' : self.subjname,
            'listgroup' : self.listgroup,
            'listname' : self.listname,
            'date_created' : self.date_created,
            'meta' : self.meta
        }

        # if extension wasn't included, add it
        if fname[-4:]!='.egg':
            fname+='.egg'

        # save
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            dd.io.save(fname, egg, compression=compression)

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

    def to_dict(self):
        egg_dict = {
            'pres' : self.pres.to_dict(orient='records'),
            'rec' : self.rec.to_dict(orient='records'),
        }
        return egg_dict

    def to_json(self):
        egg_dict = {
            'pres' : self.pres.to_json(orient='records'),
            'rec' : self.rec.to_json(orient='records'),
        }
        return egg_dict

    def analyze(self, analysis=None, **kwargs):
        """
        Calls analyze function
        """
        return analyze(self, analysis=analysis, **kwargs)

class FriedEgg(object):
    """
    Object containing results of a quail analyses

    Parameters
    ----------

    Attributes
    ----------

    data : List of Pandas.DataFrame
        List of Dataframes containing result of an analysis

    type : str
        The type of analysis (e.g. lag-crp)

    """

    def __init__(self, data=None, analysis=None, list_length=None, n_lists=None,
                 n_subjects=None, position=0, date_created=None):

        self.data = data
        self.analysis = analysis
        self.list_length = list_length
        self.n_lists = n_lists
        self.n_subjects = n_subjects
        self.position = position

        if date_created is None:
            self.date_created = time.strftime("%c")
        else:
            self.date_created = date_created

    def plot(self, **kwargs):
        return plot(self, **kwargs)

    def get_data(self):
        """
        Return a copy of the data
        """
        return self.data.copy()

    def save(self, fname, compression='blosc'):
        """
        Save method for the FriedEgg object

        The data will be saved as a 'fegg' file, which is a dictionary containing
        the elements of a FriedEgg saved in the hd5 format using
        `deepdish`.

        Parameters
        ----------

        fname : str
            A name for the file.  If the file extension (.fegg) is not specified,
            it will be appended.

        compression : str
            The kind of compression to use.  See the deepdish documentation for
            options: http://deepdish.readthedocs.io/en/latest/api_io.html#deepdish.io.save

        """

        egg = {
            'data' : self.data,
            'analysis' : self.analysis,
            'list_length' : self.list_length,
            'n_lists' : self.n_lists,
            'n_subjects' : self.n_subjects,
            'position' : self.position,
            'date_created' : self.date_created,
            'meta' : self.meta
        }

        if fname[-4:]!='.fegg':
            fname+='.fegg'

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            dd.io.save(fname, egg, compression=compression)
