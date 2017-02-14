
import pandas as pd
from analysis import recall_matrix
from helpers import list2pd


class Pyro(object):
    """
    Data object for the pyrec package

    This class contains free recall data and metadata that will be used by pyrec.

    Attributes
    ----------
    
    pres : pd.DataFrame
        Dataframe containing the presented words.  Each row represents the presented words for a given list and each column
        represents a list. The cells should be lowercase words. The index will be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number
    
    features : pd.DataFrame
        Dataframe containing the features for presented words.  Each row represents the presented words for a given list and each column
        represents a list. The cells should be a dictionary of features, where the keys are the name of the features, and the values are the feature values.
        The index will be a multi-index, where the first level reprensents the subject number and the second level represents the list number
        
    rec : pd.DataFrame
        Dataframe containing the words recalled.  Each row represents the recalled words for a given list and each column
        represents a list.  Each row represents the recalled words for a given list and each column
        represents a list. The cells should be lowercase words. The index will be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number
    
    meta : dict (optional)
        Meta data about the study (i.e. version, description, date, etc.) can be saved here
    
    """


    def __init__(self, pres=pd.DataFrame(), rec=pd.DataFrame(), meta={}):#features=pd.DataFrame(),

        self.pres=list2pd(pres)
        #self.features=features
        self.rec=list2pd(rec)
        self.meta=meta
        #self._recall_mtx = recall_matrix(self.pres, self.rec)







