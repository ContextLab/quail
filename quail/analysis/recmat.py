import numpy as np
import pandas as pd
import six
from scipy.spatial.distance import cdist
from ..helpers import check_nan, _format

def recall_matrix(egg, match='exact', distance='euclidean', features=None):
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

    if match in ['best', 'smooth']:
        if not features:
            features = [k for k,v in egg.pres.loc[0][0].values[0].items() if k!='item']
            if not features:
                raise('No features found.  Cannot match with best or smooth strategy')

    if not isinstance(features, list):
        features = [features]

    if match=='exact':
        features=['item']
        return _recmat_exact(egg.pres, egg.rec, features)
    else:
        return _recmat_smooth(egg.pres, egg.rec, features, distance, match)

def _recmat_exact(presented, recalled, features):
    lists = presented.index.get_values()
    cols = max(presented.shape[1], recalled.shape[1])
    result = np.empty((presented.shape[0], cols))*np.nan
    for li, l in enumerate(lists):
        p_list = presented.loc[l]
        r_list = recalled.loc[l]
        for i, feature in enumerate(features):
            get_feature = lambda x: np.array(x[feature]) if not np.array(pd.isnull(x['item'])).any() else np.nan
            p = np.vstack(p_list.apply(get_feature).get_values())
            r = r_list.dropna().apply(get_feature).get_values()
            r = np.vstack(list(filter(lambda x: x is not np.nan, r)))
            m = [np.where((p==x).all(axis=1))[0] for x in r]
            result[li, :len(m)] = [x[0]+1 if len(x)>0 else np.nan for x in m]
    return result

def _recmat_smooth(presented, recalled, features, distance, match):

    if match == 'best':
        func = np.argmax
    elif match == 'smooth':
        func = np.nanmean

    simmtx = _similarity_smooth(presented, recalled, features, distance)


    if match == 'best':
        recmat = np.atleast_3d([func(s, 1) for s in simmtx]).astype(np.float64)
        recmat+=1
        recmat[np.isnan(simmtx).any(2)]=np.nan
    elif match == 'smooth':
        recmat = np.atleast_3d([func(s, 0) for s in simmtx]).astype(np.float64)


    return recmat

def _similarity_smooth(presented, recalled, features, distance):
    lists = presented.index.get_values()
    res = np.empty((len(lists), len(features), recalled.iloc[0].shape[0], presented.iloc[0].shape[0]))*np.nan
    for li, l in enumerate(lists):
        p_list = presented.loc[l]
        r_list = recalled.loc[l]
        for i, feature in enumerate(features):
            get_feature = lambda x: np.array(x[feature]) if np.array(pd.notna(x['item'])).any() else np.nan
            p = np.vstack(p_list.apply(get_feature).get_values())
            r = r_list.dropna().apply(get_feature).get_values()
            r = np.vstack(list(filter(lambda x: x is not np.nan, r)))
            tmp = 1 - cdist(r, p, distance)
            res[li, i, :tmp.shape[0], :] =  tmp
    if distance == 'correlation':
        return np.nanmean(res, 1)
    else:
        return np.mean(res, 1)
