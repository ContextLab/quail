from __future__ import division
import warnings
import numpy as np
from ..distance import dist_funcs as distdict
import six

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

    inds = egg.pres.index.tolist()
    slices = [egg.crack(subjects=[i], lists=[j]) for i, j in inds]

    if features is None:
        features = egg.dist_funcs.keys()

    weights = np.zeros((len(slices), len(features)))
    for sdx, s in enumerate(slices):
        for fdx, f in enumerate(features):
            weights[sdx, fdx] = _get_weight(s, f, distdict)
    return np.nanmean(weights, axis=0)

def _get_weight(egg, feature, distdict):
    """
    Compute clustering scores along a set of feature dimensions

    Parameters
    ----------
    egg : quail.Egg

    distances : matrix
        distance matrix for a given feature

    Returns
    ----------
    weight : float
        clustering score along a particular dimension for a list
    """

    def get_distmat(egg, feature, distdict):
        from scipy.spatial.distance import cdist
        f = np.atleast_2d([xi[feature] for xi in egg.get_pres_features().as_matrix()[0]])
        if 1 in f.shape:
            f = f.T
        return cdist(f, f, distdict[egg.dist_funcs[feature]])

    pres = list(egg.get_pres_items().as_matrix()[0])
    rec = list(egg.get_rec_items().as_matrix()[0])

    if len(rec) <= 2:
        warnings.warn('Not enough recalls to compute fingerprint, returning default'
              'fingerprint.. (everything is .5)')
        return .5

    distmat = get_distmat(egg, feature, distdict)

    past_words = []
    past_idxs = []
    ranks = []
    for i in range(len(rec)-1):
        c, n = rec[i], rec[i + 1]
        if (c in pres and n in pres) and (c not in past_words and n not in past_words):
            dists = distmat[pres.index(c),:]
            cdist = dists[pres.index(n)]
            dists_filt = np.array([dist for idx, dist in enumerate(dists) if idx not in past_idxs])
            ranks.append(np.mean(np.where(np.sort(dists_filt)[::-1] == cdist)[0]+1) / len(dists_filt))
            past_idxs.append(pres.index(c))
            past_words.append(c)
    return np.nanmean(ranks)

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

def permute_fingerprint_serial(p, r, f, distances, n_perms=100):
    perms = [compute_feature_weights(p, list(np.random.permutation(r)), f, distances) for i in range(n_perms)]
    real = compute_feature_weights(p, r, f, distances)
    bools = [[f < r for f, r in zip(perm, real)] for perm in perms]
    return np.sum(np.array(bools), axis=0) / n_perms
