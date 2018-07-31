from __future__ import division
import warnings
import numpy as np
import six
from scipy.spatial.distance import cdist
from ..distance import dist_funcs as distdict
from ..helpers import shuffle_egg

def fingerprint_helper(egg, permute=False, n_perms=1000,
                       match='exact', distance='euclidean', features=None):
    """
    Computes clustering along a set of feature dimensions

    Parameters
    ----------
    egg : quail.Egg
        Data to analyze

    dist_funcs : dict
        Dictionary of distance functions for feature clustering analyses

    Returns
    ----------
    probabilities : Numpy array
      Each number represents clustering along a different feature dimension

    """

    if features is None:
        features = egg.dist_funcs.keys()

    inds = egg.pres.index.tolist()
    slices = [egg.crack(subjects=[i], lists=[j]) for i, j in inds]

    weights = _get_weights(slices, features, distdict, permute, n_perms, match,
                            distance)
    return np.nanmean(weights, axis=0)

def _get_weights(slices, features, distdict, permute, n_perms, match, distance):
    weights = np.zeros((len(slices), len(features)))
    for sdx, s in enumerate(slices):
        for fdx, f in enumerate(features):
            if match is 'exact':
                weights[sdx, fdx] = _get_weight_exact(s, f, distdict, permute,
                                                      n_perms)
            elif match is 'best':
                weights[sdx, fdx] = _get_weight_best(s, f, distdict, permute,
                                                      n_perms, distance)
    return weights

def _get_weight_exact(egg, feature, distdict, permute, n_perms):

    if permute:
        return _permute(egg, feature, distdict, _get_weight_exact, n_perms)

    pres = list(egg.get_pres_items().values[0])
    rec = list(egg.get_rec_items().values[0])

    if len(rec) <= 2:
        warnings.warn('Not enough recalls to compute fingerprint, returning default'
              'fingerprint.. (everything is .5)')
        return np.nan

    distmat = get_distmat(egg, feature, distdict)

    past_words = []
    past_idxs = []
    ranks = []
    for i in range(len(rec)-1):
        c, n = rec[i], rec[i + 1]
        if (c in pres and n in pres) and (c not in past_words and n not in past_words):
            dists = distmat[pres.index(c),:]
            di = dists[pres.index(n)]
            dists_filt = np.array([dist for idx, dist in enumerate(dists) if idx not in past_idxs])
            ranks.append(np.mean(np.where(np.sort(dists_filt)[::-1] == di)[0]+1) / len(dists_filt))
            past_idxs.append(pres.index(c))
            past_words.append(c)
    return np.nanmean(ranks)

def _get_weight_best(egg, feature, distdict, permute, n_perms, distance):

    if permute:
        return _permute(egg, feature, distdict, _get_weight_best, n_perms)

    rec = list(egg.get_rec_items().values[0])
    if len(rec) <= 2:
        warnings.warn('Not enough recalls to compute fingerprint, returning default'
              'fingerprint.. (everything is .5)')
        return np.nan

    distmat = get_distmat(egg, feature, distdict)
    matchmat = get_match(egg, feature, distdict)

    ranks = []
    for i in range(len(rec)-1):
        cdx, ndx = np.argmin(matchmat[i, :]), np.argmin(matchmat[i+1, :])
        dists = distmat[cdx, :]
        di = dists[ndx]
        dists_filt = np.array([dist for idx, dist in enumerate(dists)])
        ranks.append(np.mean(np.where(np.sort(dists_filt)[::-1] == di)[0]+1) / len(dists_filt))
    return np.nanmean(ranks)

def _get_weight_smooth(egg, feature, distdict, permute, n_perms, distance):

    if permute:
        return _permute(egg, feature, distdict, _get_weight_smooth, n_perms)

    rec = list(egg.get_rec_items().values[0])
    if len(rec) <= 2:
        warnings.warn('Not enough recalls to compute fingerprint, returning default'
              'fingerprint.. (everything is .5)')
        return np.nan

    distmat = get_distmat(egg, feature, distdict)
    matchmat = get_match(egg, feature, distdict)

    ranks = []
    for i in range(len(rec)-1):
        cdx, ndx = np.argmin(matchmat[i, :]), np.argmin(matchmat[i+1, :])
        dists = distmat[cdx, :]
        di = dists[ndx]
        dists_filt = np.array([dist for idx, dist in enumerate(dists)])
        ranks.append(np.mean(np.where(np.sort(dists_filt)[::-1] == di)[0]+1) / len(dists_filt))
    return np.nanmean(ranks)

def get_distmat(egg, feature, distdict):
    f = np.atleast_2d([xi[feature] for xi in egg.get_pres_features().values[0]])
    if 1 in f.shape:
        f = f.T
    return cdist(f, f, distdict[egg.dist_funcs[feature]])

def get_match(egg, feature, distdict):
    p = np.atleast_2d([xi[feature] for xi in egg.get_pres_features().values[0]]).T
    r = np.atleast_2d([xi[feature] for xi in egg.get_rec_features().values[0]]).T
    return cdist(p, r, distdict[egg.dist_funcs[feature]])

def compute_feature_weights(pres_list, rec_list, feature_list, distances):
    """
    Compute clustering scores along a set of feature dimensions

    Parameters
    ----------
    pres_list : list
        list of presented words

    rec_list : list
        list of recalled words

    feature_list : list
        list of feature dicts for presented words

    distances : dict
        dict of distance matrices for each feature

    Returns
    ----------
    weights : list
        list of clustering scores for each feature dimension
    """

    # initialize the weights object for just this list
    weights = {}
    for feature in feature_list[0]:
        weights[feature] = []

    # return default list if there is not enough data to compute the fingerprint
    if len(rec_list) <= 2:
        print('Not enough recalls to compute fingerprint, returning default'
              'fingerprint.. (everything is .5)')
        for feature in feature_list[0]:
            weights[feature] = .5
        return [weights[key] for key in weights]

    # initialize past word list
    past_words = []
    past_idxs = []

    # loop over words
    for i in range(len(rec_list)-1):

        # grab current word
        c = rec_list[i]

        # grab the next word
        n = rec_list[i + 1]

        # if both recalled words are in the encoding list and haven't been recalled before
        if (c in pres_list and n in pres_list) and (c not in past_words and n not in past_words):

            # for each feature
            for feature in feature_list[0]:

                # get the distance vector for the current word
                dists = distances[feature][pres_list.index(c),:]

                # distance between current and next word
                cdist = dists[pres_list.index(n)]

                # filter dists removing the words that have already been recalled
                dists_filt = np.array([dist for idx, dist in enumerate(dists) if idx not in past_idxs])

                # get indices
                avg_rank = np.mean(np.where(np.sort(dists_filt)[::-1] == cdist)[0]+1)

                # compute the weight
                weights[feature].append(avg_rank / len(dists_filt))

            # keep track of what has been recalled already
            past_idxs.append(pres_list.index(c))
            past_words.append(c)

    # average over the cluster scores for a particular dimension
    for feature in weights:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            weights[feature] = np.nanmean(weights[feature])

    return [weights[key] for key in weights]

def _permute(egg, feature, distdict, func, n_perms=100):
    perms = [func(shuffle_egg(egg), feature, distdict, False, None) for i in range(n_perms)]
    real = func(egg, feature, distdict, False, None)
    bools = [perm < real for perm in perms]
    return np.sum(np.array(bools), axis=0) / n_perms
