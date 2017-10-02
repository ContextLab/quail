#!/usr/bin/env python
import numpy as np
from scipy.spatial.distance import cdist
import warnings
from joblib import Parallel, delayed
import multiprocessing
from .egg import Egg
from .helpers import default_dist_funcs, parse_egg
from .analysis import analyze_chunk, fingerprint_helper, compute_feature_weights

class Fingerprint(object):
    """
    Class for the memory fingerprint

    A memory fingerprint can be defined as a subject's tendency to cluster their
    recall responses with respect to more than one stimulus feature dimensions.
    What is a 'stimulus feature dimension' you ask? It is simply an attribute of
    the stimulus, such as its color, category, spatial location etc.

    Parameters
    ----------

    init : quail.Egg
        Data to initialize the fingerprint instance

    features : list
        Features to consider for fingerprint analyses, defaults to all.

    state : np.array
        The current fingerprint (an array of real numbers between 0 and 1,
        inclusive) initialized to all 0.5

    n : int
        a counter specifying how many lists went into estimating the current
        fingerprint (initialize to 0)

    permute : bool
        A boolean flag specifying whether to use permutations to compute the
        fingerprint (default: True)


    dist_funcs : dict (optional)
        A dictionary of custom distance functions for stimulus features.  Each
        key should be the name of a feature
        and each value should be an inline distance function
        (e.g. `dist_funcs['feature_n'] = lambda a, b: abs(a-b)`)

    meta : dict (optional)
        Meta data about the study (i.e. version, description, date, etc.) can be
        saved here.
    """

    def __init__(self, init=None, features='all', state=None, n=0, permute=False, nperms=1000):

        self.history = []

        if init is not None:
            data = analyze_chunk(init,
                              analysis=fingerprint_helper,
                              analysis_type='fingerprint',
                              pass_features=True,
                              parallel=False)
            self.state = np.mean(data, 0)
            self.features = data.columns.values.tolist()
            self.history.append(self.state)
            n+=1
        else:
            self.state = None

        self.n = n

    def update(self, egg):
        """
        In-place method that updates fingerprint with new data

        Parameters
        ----------
        egg : quail.Egg
            Data to update fingerprint
        Returns
        ----------
        None
        """

        # increment n
        self.n+=1

        next_weights = np.mean(analyze_chunk(egg,
                          analysis=fingerprint_helper,
                          analysis_type='fingerprint',
                          pass_features=True,
                          parallel=False).as_matrix(), 0)

        if self.state is None:

            # multiply states by n
            c = self.state*self.n

            # update state
            self.state = (c+next_weights)/(self.n+1)

        else:

            self.state = next_weights

        # update the history
        self.history.append(next_weights)

    def get_features(self):
        return self.features

class OptimalPresenter(object):
    """
    A class that reorders stimuli to optimize memory performance

    A memory fingerprint can be defined as a subject's tendency to cluster their
    recall responses with respect to more than one stimulus feature dimensions.
    What is a 'stimulus feature dimension' you ask? It is simply an attribute of
    the stimulus, such as its color, category, spatial location etc.

    Parameters
    ----------

    init : quail.Egg
        Data to initialize the fingerprint instance

    features : list
        Features to consider for fingerprint analyses, defaults to all.

    state : np.array
        The current fingerprint (an array of real numbers between 0 and 1,
        inclusive) initialized to all 0.5

    n : int
        a counter specifying how many lists went into estimating the current
        fingerprint (initialize to 0)

    permute : bool
        A boolean flag specifying whether to use permutations to compute the
        fingerprint (default: True)


    dist_funcs : dict (optional)
        A dictionary of custom distance functions for stimulus features.  Each
        key should be the name of a feature
        and each value should be an inline distance function
        (e.g. `dist_funcs['feature_n'] = lambda a, b: abs(a-b)`)

    meta : dict (optional)
        Meta data about the study (i.e. version, description, date, etc.) can be
        saved here.
    """

    def __init__(self, strategy='random', features=None, params=None,
                 fingerprint=None):

        # set default params
        self.params = {
                        'alpha' : 4,
                        'tau' : 1,
                        'fingerprint' : Fingerprint()
                        }

        # update with user defined params
        if params is not None:
            self.params.update(params)

        self.strategy = strategy

    def set_params(self, name, value):
        """
        Sets a parameter to a particular value
        """
        self[name]=value

    def get_params(self, name):
        """
        Sets a parameter to a particular value
        """
        return self.params[name]

    def set_strategy(self, strategy='random'):
        """
        Sets a reordering strategy
        """
        self.set_strategy = strategy

    def order(self, egg, method='permute', nperms=10000, strategy=None):
        """
        Reorders a list of stimuli to match a fingerprint

        Parameters
        ----------
        egg : quail.Egg
            Data to compute fingerprint

        method : str
            Method to re-sort list. Can be 'stick' or 'permute' (default: permute)

        nperms : int
            Number of permutations to use. Only used if method='permute'. (default:
            10,000)

        strategy : str or None
            The strategy to use to reorder the list.  This can be 'stabilize',
            'destabilize', 'random' or None.  If None, the self.strategy field
            will be used. (default: None)

        Returns
        ----------
        egg : quail.Egg
            Egg re-sorted to match fingerprint
        """

        def order_perm_parallel(self, egg, distances, strategy, nperms=10000):
            """
            This function re-sorts a list by computing permutations of a given
            list and choosing the one that maximizes/minimizes variance.
            """

            # parse egg
            pres, rec, features, dist_funcs = parse_egg(egg)

            # length of list
            pres_len = len(pres)

            results = Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(run_perm)(pres, features, distances) for i in range(nperms))

            weights = np.array(map(lambda x: x[0], results))
            orders = np.array(map(lambda x: x[1], results))

            # get the fingerprint state
            fingerprint = self.get_params('fingerprint').state

            # find the closest (or farthest)
            if strategy is 'stabilize':
                closest = orders[np.argmin(cdist(np.array(fingerprint, ndmin=2), weights)),:].astype(int).tolist()
            elif strategy is 'destabilize':
                closest = orders[np.argmax(cdist(np.array(fingerprint, ndmin=2), weights)),:].astype(int).tolist()

            # return a re-sorted egg
            return Egg(pres=[list(pres[closest])], rec=[list(pres[closest])], features=[list(features[closest])])

        def order_best_stick(self, egg, distances, strategy, nperms):

            # parse egg
            pres, rec, features, dist_funcs = parse_egg(egg)

            # compute distances
            # distances = compute_distances(pres, features, dist_funcs)

            # length of list
            pres_len = len(pres)

            results = Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(stick_perm)(self, egg, distances, strategy) for i in range(nperms))

            weights = np.array(map(lambda x: x[0], results))
            orders = np.array(map(lambda x: x[1], results))

            # get the fingerprint state
            fingerprint = self.get_params('fingerprint').state

            # find the closest (or farthest)
            if strategy is 'stabilize':
                closest = orders[np.argmin(cdist(np.array(fingerprint, ndmin=2), weights)),:].astype(int).tolist()
            elif strategy is 'destabilize':
                closest = orders[np.argmax(cdist(np.array(fingerprint, ndmin=2), weights)),:].astype(int).tolist()

            # return a re-sorted egg
            return Egg(pres=[list(pres[closest])], rec=[list(pres[closest])], features=[list(features[closest])])

        # if strategy is not set explicitly, default to the class strategy
        if strategy is None:
            strategy = self.strategy

        distances = compute_distances(egg)

        if strategy is 'random':
            return shuffle_egg(egg)
        elif method is 'permute':
            return order_perm_parallel(self, egg, distances, strategy, nperms)
        elif method is 'stick':
            return order_stick(self, egg, distances, strategy)
        elif method is 'best_stick':
            return order_best_stick(self, egg, distances, strategy, nperms)

def order_stick(presenter, egg, distances, strategy):
    """
    Reorders a list according to strategy
    """

    def compute_feature_stick(features, weights, alpha):
        '''create a 'stick' of feature weights'''

        feature_stick = []
        for f, w in zip(features, weights):
            feature_stick+=[f]*int(np.power(w,alpha)*100)

        return feature_stick

    def reorder_list(egg, feature_stick, distances, tau):

        def compute_stimulus_stick(s, tau):
            '''create a 'stick' of feature weights'''

            feature_stick = [[weights[feature]]*round(weights[feature]**alpha)*100 for feature in w]
            return [item for sublist in feature_stick for item in sublist]

        # parse egg
        pres, rec, features, dist_funcs = parse_egg(egg)

        # turn pres and features into np arrays
        pres_arr = np.array(pres)
        features_arr = np.array(features)

        # starting with a random word
        reordered_list = []
        reordered_features = []

        # start with a random choice
        idx = np.random.choice(len(pres), 1)[0]

        # original inds
        inds = range(len(pres))

        # keep track of the indices
        inds_used = [idx]

        # get the word
        current_word = pres[idx]

        # get the features dict
        current_features = features[idx]

        # append that word to the reordered list
        reordered_list.append(current_word)

        # append the features to the reordered list
        reordered_features.append(current_features)

        # loop over the word list
        for i in range(len(pres)-1):

            # sample from the stick
            feature_sample = feature_stick[np.random.choice(len(feature_stick), 1)[0]]

            # indices left
            inds_left = filter(lambda ind: ind not in inds_used, inds)

            # make a copy of the words filtering out the already used ones
            words_left = pres[inds_left]

            # get word distances for the word
            dists_left = distances[feature_sample][idx, inds_left]

            # features left
            features_left = features[inds_left]

            # normalize distances
            dists_left_max = np.max(dists_left)
            if dists_left_max>0:
                dists_left_norm = dists_left/np.max(dists_left)
            else:
                dists_left_norm = dists_left

            # get the min
            dists_left_min = np.min(-dists_left_norm)

            # invert the word distances to turn distance->similarity
            dists_left_inv = - dists_left_norm - dists_left_min + .01

            # create a word stick
            words_stick = []
            for word, dist in zip(words_left, dists_left_inv):
                words_stick+=[word]*int(np.power(dist,tau)*100)

            next_word = np.random.choice(words_stick)

            next_word_idx = np.where(pres==next_word)[0]

            inds_used.append(next_word_idx)

            reordered_list.append(next_word)
            reordered_features.append(features[next_word_idx][0])

        return Egg(pres=[reordered_list], rec=[reordered_list], features=[[reordered_features]])

    # parse egg
    pres, rec, features, dist_funcs = parse_egg(egg)

    # get params needed for list reordering
    features = presenter.get_params('fingerprint').get_features()
    alpha = presenter.get_params('alpha')
    tau = presenter.get_params('tau')
    weights = presenter.get_params('fingerprint').state

    # invert the weights if strategy is destabilize
    if strategy is 'destabilize':
        weights = 1 - weights

    # compute feature stick
    feature_stick = compute_feature_stick(features, weights, alpha)

    # reorder list
    return reorder_list(egg, feature_stick, distances, tau)

# function to run 1 perm for parallel list re-sorting function
def run_perm(pres, features, distances):

    # seed RNG
    np.random.seed()

    # shuffle inds
    idx = np.random.permutation(len(pres))

    # shuffled pres
    pres_perm = list(pres[idx])

    # shuffled features
    features_perm = list(features[idx])

    # create a copy of distances
    distances_perm = distances.copy()

    for key in distances_perm:
        distances_perm[key]=distances_perm[key][idx]

    # compute weights
    weights = compute_feature_weights(pres_perm, pres_perm, features_perm, distances_perm)

    # save out the order
    orders = idx

    return weights, orders

def stick_perm(presenter, egg, distances, strategy):
    """Computes weights for one reordering using stick-breaking method"""

    # seed RNG
    np.random.seed()

    # unpack egg
    egg_pres, egg_rec, egg_features, egg_dist_funcs = parse_egg(egg)

    # reorder
    regg = order_stick(presenter, egg, distances, strategy)

    # unpack regg
    regg_pres, regg_rec, regg_features, regg_dist_funcs = parse_egg(regg)

    # get the order
    regg_pres = list(regg_pres)
    egg_pres = list(egg_pres)
    idx = [egg_pres.index(r) for r in regg_pres]

    # create a copy of distances
    distances_perm = distances.copy()

    for key in distances_perm:
        distances_perm[key]=distances_perm[key][idx]

    # compute weights
    weights = compute_feature_weights(list(regg_pres), list(regg_pres), list(regg_features), distances_perm)

    # save out the order
    orders = idx

    return weights, orders

def shuffle_egg(egg):
    """ Shuffle an Egg's recalls"""

    pres, rec, features, dist_funcs = parse_egg(egg)

    if pres.ndim==1:
        pres = pres.reshape(1, pres.shape[0])
        rec = rec.reshape(1, rec.shape[0])
        features = features.reshape(1, features.shape[0])

    for ilist in range(rec.shape[0]):
        idx = np.random.permutation(rec.shape[1])
        rec[ilist,:] = rec[ilist,idx]

    return Egg(pres=pres, rec=rec, features=features, dist_funcs=dist_funcs)

def compute_distances(egg):
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

    pres, rec, features, dist_funcs = parse_egg(egg)
    pres_list = list(pres)
    feature_list = list(features)

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
                dists[idx1,idx2] = dist_funcs[feature](feature_list[idx1][feature],feature_list[idx2][feature])

        # set that distance matrix to the value of a dict where the feature name is the key
        distances[feature] = dists

    return distances
#     def order_perm(self, egg, nperms=10000):
#         """
#         This function re-sorts a list by computing permutations of a given
#         list and choosing the one that maximizes/minimizes variance.
#         """
#
#         # parse egg
#         pres, rec, features, dist_funcs = parse_egg(egg)
#
#         # compute distances
#         distances = compute_distances(pres, features, dist_funcs)
#
#         # length of list
#         pres_len = len(pres)
#
#         # initialize weights
#         weights = np.zeros((nperms, len(features[0].keys())))
#
#         # orders are nperms shuffled indexes
#         orders  = np.zeros((nperms, pres_len))
#
#         # loop over number of permuations
#         for perm in range(nperms):
#
#             # shuffle inds
#             idx = np.random.permutation(pres_len)
#
#             # shuffled pres
#             pres_perm = list(pres[idx])
#
#             # shuffled features
#             features_perm = list(features[idx])
#
#             # create a copy of distances
#             distances_perm = distances.copy()
#
#             for key in distances_perm:
#                 distances_perm[key]=distances_perm[key][idx]
#
#             # compute weights
#             weights[perm,:] = compute_feature_weights(pres_perm, pres_perm, features_perm, distances_perm)
#
#             # save out the order
#             orders[perm,:] = idx
#
#         # get the fingerprint state
#         fingerprint = self.get_params('fingerprint').state
#
#         # find the closest
#         closest = orders[np.argmin(cdist(np.array(fingerprint, ndmin=2), weights)),:].astype(int).tolist()
#
#         # return a re-sorted egg
#         return Egg(pres=[list(pres[closest])], rec=[list(pres[closest])], features=[list(features[closest])])
#
