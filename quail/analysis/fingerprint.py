import warnings
import numpy as np
from ..distance import dist_funcs as dist_funcs_dict

# fingerprint analysis
def fingerprint_helper(pres_slice, rec_slice, feature_slice, dist_funcs, permute=False, n_perms=1000):
    """
    Computes clustering along a set of feature dimensions

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed
    feature_slice : Pandas Dataframe
        chunk of features data to be analyzed
    dist_funcs : dict
        Dictionary of distance functions for feature clustering analyses

    Returns
    ----------
    probabilities : numpy array
      each number represents clustering along a different feature dimension

    """

    # compute fingerprint for each list within a chunk
    fingerprint_matrix = []

    for p, r, f in zip(pres_slice.as_matrix(), rec_slice.as_matrix(), feature_slice.as_matrix()):

        # turn arrays into lists
        p = list(p)
        f = list(f)
        r = list([ri for ri in list(r) if isinstance(ri, str)])

        if len(r)>1:

            # compute distances
            distances = compute_distances(p, f, dist_funcs, dist_funcs_dict)

            # add optional bootstrapping
            if permute:
                fingerprint_matrix.append(permute_fingerprint_serial(p, r, f, distances, n_perms=n_perms))
            else:
                fingerprint_matrix.append(compute_feature_weights(p, r, f, distances))
        else:
            fingerprint_matrix.append([np.nan]*len(list(f[0].keys())))

    # return average over rows
    return np.mean(fingerprint_matrix, axis=0)

# fingerprint + temporal clustering analysis
def fingerprint_temporal_helper(pres_slice, rec_slice, feature_slice, dist_funcs, permute=True, n_perms=1000):
    """
    Computes clustering along a set of feature dimensions

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed
    feature_slice : Pandas Dataframe
        chunk of features data to be analyzed
    dist_funcs : dict
        Dictionary of distance functions for feature clustering analyses

    Returns
    ----------
    probabilities : numpy array
      each number represents clustering along a different feature dimension

    """
    # compute fingerprint for each list within a chunk
    fingerprint_matrix = []

    for p, r, f in zip(pres_slice.as_matrix(), rec_slice.as_matrix(), feature_slice.as_matrix()):

        # turn arrays into lists
        p = list(p)
        f = list(f)
        r = list([ri for ri in list(r) if isinstance(ri, str)])

        # add in temporal clustering
        nf = []
        for idx, fi in enumerate(f):
            fi['temporal'] = idx
            nf.append(fi)

        dist_funcs_copy = dist_funcs.copy()
        dist_funcs_copy['temporal'] = 'lambda a, b : np.abs(a-b)'

        # if there is at least 1 transition
        if len(r)>1:

            # compute distances
            distances = compute_distances(p, nf, dist_funcs_copy, dist_funcs_dict)

            # add optional bootstrapping
            if permute:
                fingerprint_matrix.append(permute_fingerprint_serial(p, r, nf, distances, n_perms=n_perms))
            else:
                fingerprint_matrix.append(compute_feature_weights(p, r, nf, distances))
        else:
            fingerprint_matrix.append([np.nan]*len(list(nf[0].keys())))

    return np.nanmean(fingerprint_matrix, axis=0)

def compute_distances(pres_list, feature_list, dist_funcs, dist_funcs_dict):
    """
    Compute distances between list words along n feature dimensions

    Parameters
    ----------
    pres_list : list
        list of presented words
    feature_list : list
        list of feature dicts for presented words
    dist_funcs : dict
        dict of distance functions for each feature

    Returns
    ----------
    distances : dict
        dict of distance matrices for each feature
    """

    # initialize dist dict
    distances = {}

    # for each feature in dist_funcs
    for feature in dist_funcs:

        # initialize dist matrix
        dists = np.zeros((len(pres_list), len(pres_list)))

        # for each word in the list
        for idx1, item1 in enumerate(pres_list):

            # for each word in the list
            for idx2, item2 in enumerate(pres_list):

                # compute the distance between word 1 and word 2 along some feature dimension
                dists[idx1,idx2] = dist_funcs_dict[dist_funcs[feature]](feature_list[idx1][feature],feature_list[idx2][feature])

        # set that distance matrix to the value of a dict where the feature name is the key
        distances[feature] = dists

    return distances

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
        print('Not enough recalls to compute fingerprint, returning default fingerprint.. (everything is .5)')
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

    r_perms = []
    r_real = compute_feature_weights(p, r, f, distances)

    for iperm in range(n_perms):
        r_perm = list(np.random.permutation(r))
        r_perms.append(compute_feature_weights(p, r_perm, f, distances))

    r_perms_bool = []
    for perm in r_perms:
        r_perm_bool = []
        for idx, feature_perm in enumerate(perm):
            r_perm_bool.append(feature_perm < r_real[idx])
        r_perms_bool.append(r_perm_bool)

    return np.sum(np.array(r_perms_bool), axis=0) / n_perms
