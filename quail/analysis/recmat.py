import numpy as np
import pandas as pd
import six
from scipy.spatial.distance import cdist
from ..helpers import check_nan, _format

def recall_matrix(egg, match='exact', distance='euclidean',
                  features=None):
    """
    Computes recall matrix given list of presented and list of recalled words

    Parameters
    ----------
    egg : quail.Egg
        Data to analyze

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
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists

    """
    def recmat(presented, recalled, match, distance):
        result = np.empty(recalled.shape)
        for idx, (p, r) in enumerate(zip(presented, recalled)):
            if match is 'exact':
                m = [np.where(x==p)[0] for x in r]
                result[idx,:] = [x[0]+1 if len(x)>0 else np.nan for x in m]
            elif match is 'best':
                p, r = _format(p, r)
                result = - cdist(r, p, distance)
            elif match is 'smooth':
                p, r = _format(p, r)
                result = - cdist(r, p, distance)
        return result

    def feature_filter(presented, recalled, feature):
        presented = presented.applymap(lambda x: x[feature]).values
        recalled = recalled.applymap(lambda x: x[feature] if x['item'] is not np.nan else np.nan).values
        return presented, recalled

    def recmat_by_feature(presented, recalled, feature, match, distance):
        p, r = feature_filter(presented, recalled, feature)
        return recmat(p, r, match, distance)

    presented = egg.pres
    recalled = egg.rec

    if match in ['best', 'smooth']:
        if not features:
            features = [k for k,v in presented.loc[0][0].values[0].items() if k!='item']
            if not features:
                raise('No features found.  Cannot match with best or smooth strategy')

    if not isinstance(features, list):
        features = [features]

    result = np.mean([recmat_by_feature(presented, recalled, feature, match,
                                        distance) for feature in features], 0)

    if match is 'best':
        result = np.argmax(result, 1)+1
    elif match is 'smooth':
        pass

    return np.atleast_2d(result)
