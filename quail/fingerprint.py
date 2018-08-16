#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from builtins import zip
from builtins import range
from builtins import object
import numpy as np
from scipy.spatial.distance import cdist
import warnings
from joblib import Parallel, delayed
import multiprocessing
from .egg import Egg
from .helpers import default_dist_funcs, parse_egg, shuffle_egg
from .analysis.analysis import _analyze_chunk
from .analysis.clustering import fingerprint_helper, _get_weights
from .distance import dist_funcs as builtin_dist_funcs

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

    def __init__(self, init=None, features='all', state=None, n=0,
                 permute=False, nperms=1000, parallel=False):

        self.history = []

        if init is not None:
            data = _analyze_chunk(init,
                                analysis=fingerprint_helper,
                                analysis_type='fingerprint',
                                pass_features=True,
                                permute=permute,
                                n_perms=nperms,
                                parallel=parallel)
            self.state = np.mean(data, 0)
            self.features = data.columns.values.tolist()
            self.history.append(self.state)
            n+=1
        else:
            self.state = None
            self.features = None

        self.n = n

    def update(self, egg, permute=False, nperms=1000,
                 parallel=False):
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

        next_weights = np.nanmean(_analyze_chunk(egg,
                          analysis=fingerprint_helper,
                          analysis_type='fingerprint',
                          pass_features=True,
                          permute=permute,
                          n_perms=nperms,
                          parallel=parallel).values, 0)

        if self.state is not None:

            # multiply states by n
            c = self.state*self.n

            # update state
            self.state = np.nansum(np.array([c, next_weights]), axis=0)/(self.n+1)

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
        self.params[name]=value

    def get_params(self, name):
        """
        Sets a parameter to a particular value
        """
        return self.params[name]

    def set_strategy(self, strategy='random'):
        """
        Sets a reordering strategy
        """

        self.strategy = strategy

    def order(self, egg, method='permute', nperms=2500, strategy=None,
              distfun='correlation', fingerprint=None):
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
            2500)

        strategy : str or None
            The strategy to use to reorder the list.  This can be 'stabilize',
            'destabilize', 'random' or None.  If None, the self.strategy field
            will be used. (default: None)

        distfun : str or function
            The distance function to reorder the list fingerprint to the target
            fingerprint.  Can be any distance function supported by
            scipy.spatial.distance.cdist. For more info, see:
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
            (default: euclidean)

        fingerprint : quail.Fingerprint or np.array
            Fingerprint (or just the state of a fingerprint) to reorder by. If
            None, the list will be reordered according to the fingerprint
            attached to the presenter object.

        Returns
        ----------
        egg : quail.Egg
            Egg re-sorted to match fingerprint
        """

        def order_perm(self, egg, dist_dict, strategy, nperm, distperm,
                       fingerprint):
            """
            This function re-sorts a list by computing permutations of a given
            list and choosing the one that maximizes/minimizes variance.
            """

            # parse egg
            pres, rec, features, dist_funcs = parse_egg(egg)

            # length of list
            pres_len = len(pres)

            weights = []
            orders = []
            for i in range(nperms):
                x = rand_perm(pres, features, dist_dict, dist_funcs)
                weights.append(x[0])
                orders.append(x[1])
            weights = np.array(weights)
            orders = np.array(orders)

            # find the closest (or farthest)
            if strategy=='stabilize':
                closest = orders[np.nanargmin(cdist(np.array(fingerprint, ndmin=2), weights, distperm)),:].astype(int).tolist()
            elif strategy=='destabilize':
                closest = orders[np.nanargmax(cdist(np.array(fingerprint, ndmin=2), weights, distperm)),:].astype(int).tolist()

            # return a re-sorted egg
            return Egg(pres=[list(pres[closest])], rec=[list(pres[closest])], features=[list(features[closest])])

        def order_best_stick(self, egg, dist_dict, strategy, nperms, distfun,
                             fingerprint):

            # parse egg
            pres, rec, features, dist_funcs = parse_egg(egg)

            results = Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(stick_perm)(self, egg, dist_dict, strategy) for i in range(nperms))

            weights = np.array([x[0] for x in results])
            orders = np.array([x[1] for x in results])

            # find the closest (or farthest)
            if strategy=='stabilize':
                closest = orders[np.nanargmin(cdist(np.array(fingerprint, ndmin=2), weights, distfun)),:].astype(int).tolist()
            elif strategy=='destabilize':
                closest = orders[np.nanargmax(cdist(np.array(fingerprint, ndmin=2), weights, distfun)),:].astype(int).tolist()

            # return a re-sorted egg
            return Egg(pres=[list(pres[closest])], rec=[list(pres[closest])], features=[list(features[closest])], dist_funcs=dist_funcs)

        def order_best_choice(self, egg, dist_dict, nperms, distfun,
                              fingerprint):

            # get strategy
            strategy = self.strategy

            # parse egg
            pres, rec, features, dist_funcs = parse_egg(egg)

            results = Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(choice_perm)(self, egg, dist_dict) for i in range(nperms))

            weights = np.array([x[0] for x in results])
            orders = np.array([x[1] for x in results])

            # find the closest (or farthest)
            if strategy=='stabilize':
                closest = orders[np.nanargmin(cdist(np.array(fingerprint, ndmin=2), weights, distfun)),:].astype(int).tolist()
            elif strategy=='destabilize':
                closest = orders[np.nanargmax(cdist(np.array(fingerprint, ndmin=2), weights, distfun)),:].astype(int).tolist()

            # return a re-sorted egg
            return Egg(pres=[list(pres[closest])], rec=[list(pres[closest])], features=[list(features[closest])], dist_funcs=dist_funcs)

        # if strategy is not set explicitly, default to the class strategy
        if strategy is None:
            strategy = self.strategy

        dist_dict = compute_distances_dict(egg)

        if fingerprint is None:
            fingerprint = self.get_params('fingerprint').state
        elif isinstance(fingerprint, Fingerprint):
            fingerprint = fingerprint.state
        else:
            print('using custom fingerprint')

        if (strategy=='random') or (method=='random'):
            return shuffle_egg(egg)
        elif method=='permute':
            return order_perm(self, egg, dist_dict, strategy, nperms, distfun,
                              fingerprint) #
        elif method=='stick':
            return order_stick(self, egg, dist_dict, strategy, fingerprint) #
        elif method=='best_stick':
            return order_best_stick(self, egg, dist_dict, strategy, nperms,
                                    distfun, fingerprint) #
        elif method=='best_choice':
            return order_best_choice(self, egg, dist_dict, nperms,
                                     fingerprint) #

def order_stick(presenter, egg, dist_dict, strategy, fingerprint):
    """
    Reorders a list according to strategy
    """

    def compute_feature_stick(features, weights, alpha):
        '''create a 'stick' of feature weights'''

        feature_stick = []
        for f, w in zip(features, weights):
            feature_stick+=[f]*int(np.power(w,alpha)*100)

        return feature_stick

    def reorder_list(egg, feature_stick, dist_dict, tau):

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
        inds = list(range(len(pres)))

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
            inds_left = [ind for ind in inds if ind not in inds_used]

            # make a copy of the words filtering out the already used ones
            words_left = pres[inds_left]

            # get word distances for the word
            dists_left = np.array([dist_dict[current_word][word][feature_sample] for word in words_left])

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

        return Egg(pres=[reordered_list], rec=[reordered_list], features=[[reordered_features]], dist_funcs=dist_funcs)

    # parse egg
    pres, rec, features, dist_funcs = parse_egg(egg)

    # get params needed for list reordering
    features = presenter.get_params('fingerprint').get_features()
    alpha = presenter.get_params('alpha')
    tau = presenter.get_params('tau')
    weights = fingerprint

    # invert the weights if strategy is destabilize
    if strategy=='destabilize':
        weights = 1 - weights

    # compute feature stick
    feature_stick = compute_feature_stick(features, weights, alpha)

    # reorder list
    return reorder_list(egg, feature_stick, dist_dict, tau)

def order_choice(presenter, egg, dist_dict, fingerprint):

    # get strategy
    strategy = presenter.strategy

    # get tau
    tau = presenter.get_params('tau')

    # get number of features
    nfeats = len(presenter.get_params('fingerprint').features)

    # parse egg
    pres, rec, features, dist_funcs = parse_egg(egg)

    # start with a random word
    idx = np.random.choice(len(pres), 1)[0]

    # original inds
    inds = list(range(len(pres)))

    # keep track of the indices
    inds_used = [idx]

    # get the word
    current_word = pres[idx]

    # get the features dict
    current_features = features[idx]

    # append that word to the reordered list
    reordered_list = [current_word]

    # append the features to the reordered list
    reordered_features = [current_features]

    # loop over the word list
    for i in range(len(pres)-1):

        # indices left
        inds_left = [ind for ind in inds if ind not in inds_used]

        # make a copy of the words filtering out the already used ones
        words_left = pres[inds_left]

        # features left
        features_left = features[inds_left]

        # get weights if each word was added
        idx=0
        weights = np.zeros((len(words_left), nfeats))
        for word, feat in zip(words_left, features_left):
            weights[idx,:]=compute_feature_weights_dict(
                list(pres),
                reordered_list+[word],
                reordered_features+[feat],
                dist_dict)
            idx+=1

        # print(weights)
        # print(cdist(np.array(fingerprint, ndmin=2), weights, 'euclidean'))

        # pick the closest (or farthest)
        # if strategy is 'stabilize':
        # pick = np.argmin(cdist(np.array(fingerprint, ndmin=2), weights, 'euclidean'))
        stick = []
        dist = cdist(np.array(fingerprint, ndmin=2), weights, 'correlation').reshape(len(words_left), 1)
        for idx, val in enumerate(dist):
            for i in range(int((val*tau)*100)):
                stick.append(idx)
        pick = np.random.choice(stick, 1)[0]
        # elif strategy is 'destabilize':
        #     pick = np.argmin(cdist(np.array(fingerprint, ndmin=2), weights, 'euclidean'))

        # get the next word
        next_word = words_left[pick]

        # and the idx of the next word
        next_word_idx = np.where(pres==next_word)[0]

        # append it to the inds already used
        inds_used.append(next_word_idx)

        # update the list
        reordered_list.append(next_word)
        reordered_features.append(features[next_word_idx][0])

    return Egg(pres=[reordered_list], rec=[reordered_list], features=[[reordered_features]], dist_funcs=dist_funcs)

# function to run 1 perm for parallel list re-sorting function
def rand_perm(pres, features, dist_dict, dist_funcs):

    # seed RNG
    np.random.seed()

    # shuffle inds
    idx = np.random.permutation(len(pres))

    # shuffled pres
    pres_perm = list(pres[idx])

    # shuffled features
    features_perm = list(features[idx])

    # compute weights
    weights = compute_feature_weights_dict(pres_perm, pres_perm, features_perm, dist_dict)

    # save out the order
    orders = idx

    return weights, orders

def stick_perm(presenter, egg, dist_dict, strategy):
    """Computes weights for one reordering using stick-breaking method"""

    # seed RNG
    np.random.seed()

    # unpack egg
    egg_pres, egg_rec, egg_features, egg_dist_funcs = parse_egg(egg)

    # reorder
    regg = order_stick(presenter, egg, dist_dict, strategy)

    # unpack regg
    regg_pres, regg_rec, regg_features, regg_dist_funcs = parse_egg(regg)

    # # get the order
    regg_pres = list(regg_pres)
    egg_pres = list(egg_pres)
    idx = [egg_pres.index(r) for r in regg_pres]

    # compute weights
    weights = compute_feature_weights_dict(list(regg_pres), list(regg_pres), list(regg_features), dist_dict)

    # save out the order
    orders = idx

    return weights, orders

def choice_perm(presenter, egg, dist_dict):
    """
    Reorder a list by iteratively selecting words that get closer to the
    target fingerprint
    """
    # seed RNG
    np.random.seed()

    strategy = presenter.strategy

    # unpack egg
    egg_pres, egg_rec, egg_features, egg_dist_funcs = parse_egg(egg)

    # reorder
    regg = order_choice(presenter, egg, dist_dict)

    # unpack regg
    regg_pres, regg_rec, regg_features, regg_dist_funcs = parse_egg(regg)

    # get the order
    regg_pres = list(regg_pres)
    egg_pres = list(egg_pres)
    idx = [egg_pres.index(r) for r in regg_pres]

    # compute weights
    weights = compute_feature_weights_dict(list(regg_pres), list(regg_pres), list(regg_features), dist_dict)

    # save out the order
    orders = idx

    return weights, orders

def compute_distances_dict(egg):
    """ Creates a nested dict of distances """
    pres, rec, features, dist_funcs = parse_egg(egg)
    pres_list = list(pres)
    features_list = list(features)

    # initialize dist dict
    distances = {}

    # for each word in the list
    for idx1, item1 in enumerate(pres_list):

        distances[item1]={}

        # for each word in the list
        for idx2, item2 in enumerate(pres_list):

            distances[item1][item2]={}

            # for each feature in dist_funcs
            for feature in dist_funcs:
                distances[item1][item2][feature] = builtin_dist_funcs[dist_funcs[feature]](features_list[idx1][feature],features_list[idx2][feature])

    return distances

def compute_feature_weights_dict(pres_list, rec_list, feature_list, dist_dict):
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
    if len(rec_list) < 2:
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
                # dists = [dist_dict[c][j][feature] for j in dist_dict[c]]
                # distance between current and next word
                c_dist = dist_dict[c][n][feature]

                # filter dists removing the words that have already been recalled
                # dists_filt = np.array([dist for idx, dist in enumerate(dists) if idx not in past_idxs])
                dists_filt = [dist_dict[c][j][feature] for j in dist_dict[c] if j not in past_words]

                # get indices
                avg_rank = np.mean(np.where(np.sort(dists_filt)[::-1] == c_dist)[0]+1)

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
