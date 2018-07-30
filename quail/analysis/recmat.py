import numpy as np
import pandas as pd
import six
import hypertools as hyp
from scipy.spatial.distance import cdist
from ..helpers import check_nan, _format

def recall_matrix(egg, match='exact', distance='euclidean',
                  features=None, whiten=False):
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

    whiten : bool
        If True, the recall model will be whitened by the pres model.


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

    result = np.nanmean([_recmat_by_feature(egg.pres, egg.rec, feature, match,
                                        distance) for feature in features], 0)
    return np.atleast_2d(result)

def _recmat_by_feature(presented, recalled, feature, match, distance):
    p, r = _feature_filter(presented, recalled, feature)
    return _recmat(p, r, match, distance)

def _feature_filter(presented, recalled, feature):
    presented = presented.applymap(lambda x: x[feature])
    recalled = recalled.applymap(lambda x: x[feature] if x['item'] is not np.nan else np.nan)
    return presented, recalled


def _recmat(presented, recalled, match, distance, whiten=False):
    if match in ('exact', 'best'):
        cols = max(presented.shape[1], recalled.shape[1])
        result = np.empty((presented.shape[0], cols))*np.nan
    else:
        result = np.empty(tuple(list(presented.shape)+[recalled.shape[1]]))*np.nan

    for i, idx in enumerate(presented.index.get_values()):
        p = np.stack(presented.loc[idx].get_values())
        r = np.stack(recalled.loc[idx].dropna().get_values())
        if (p.ndim==1 or r.ndim==1):
            p = np.atleast_2d(p).T
            r = np.atleast_2d(r).T
        if match is 'exact':
            m = [np.where((p==x).all(axis=1))[0] for x in r]
            result[i, :len(m)] = [x[0]+1 if len(x)>0 else np.nan for x in m]
        elif match is 'best':
            res = np.empty(p.shape[0])*np.nan
            tmp = 1 - cdist(r, p, distance)
            tmp = np.array(np.argmax(tmp, 1)+1).astype(np.float64)
            res[:r.shape[0]]=tmp
            result[i, :] = res
        elif match is 'smooth':
            tmp = 1 - cdist(r, p, distance)
            result[i, :, :tmp.shape[0]] = tmp.T
    return result

def _whiten(X, recmat):
    # return np.dot(np.linalg.inv(np.corrcoef(p)), recmat.T).T

   # get the covariance matrix
   X_norm = hyp.normalize(X, normalize='within')
   Xcov = np.dot(X_norm, X_norm.T)

   # eigenvalue decomposition of the covariance matrix
   d, V = np.linalg.eigh(Xcov)

   # a fudge factor can be used so that eigenvectors associated with
   # small eigenvalues do not get overamplified.
   D = np.diag(1. / np.sqrt(d+.00001))

   # whitening matrix
   W = np.dot(np.dot(V, D), V.T)

   # multiply by the whitening matrix
   return np.dot(recmat, W)

# result = np.empty(recalled.shape)
# for idx, (p, r) in enumerate(zip(presented, recalled)):
#     if match is 'exact':
#         m = [np.where(x==p)[0] for x in r]
#         result[idx, :] = [x[0]+1 if len(x)>0 else np.nan for x in m]
#     elif match is 'best':
#         p, r = _format(p, r)
#         tmp = 1 - cdist(r, p, distance)
#         nans = np.argwhere(np.isnan(tmp))
#         tmp = np.array(np.argmax(tmp, 1)+1).astype(np.float64)
#         if nans!=[]:
#             tmp[np.unique(nans[:,0])]=np.nan
#         result[idx, :] = tmp
#     elif match is 'smooth':
#         p, r = _format(p, r)
#         result[idx, :] = np.mean(1 - cdist(r, p, distance), 0)
# return result
