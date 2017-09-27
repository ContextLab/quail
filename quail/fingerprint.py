#!/usr/bin/env python
import numpy as np
from scipy.spatial.distance import cdist
import warnings
from .egg import Egg
from .helpers import default_dist_funcs, parse_egg
from .analysis import analyze_chunk, fingerprint_helper, compute_distances, compute_feature_weights

class Fingerprint(object):
    """
    Class for the memory fingerprint and associated functions

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

    def order_perm(self, egg, nperms=10000):
        """
        This function re-sorts a list by computing permutations of a given
        list and choosing the one that maximizes/minimizes variance.
        """

        # parse egg
        pres, rec, features, dist_funcs = parse_egg(egg)

        # compute distances
        distances = compute_distances(pres, features, dist_funcs)

        # length of list
        pres_len = len(pres)

        # initialize weights
        weights = np.zeros((nperms, len(features[0].keys())))

        # orders are nperms shuffled indexes
        orders  = np.zeros((nperms, pres_len))

        # loop over number of permuations
        for perm in range(nperms):

            # shuffle inds
            idx = np.random.permutation(pres_len)

            # shuffled pres
            pres_perm = list(pres[idx])

            # shuffled features
            features_perm = list(features[idx])

            # create a copy of distances
            distances_perm = distances.copy()

            for key in distances_perm:
                distances_perm[key]=distances_perm[key][idx]

            # compute weights
            weights[perm,:] = compute_feature_weights(pres_perm, pres_perm, features_perm, distances_perm)

            # save out the order
            orders[perm,:] = idx

        # get the fingerprint state
        fingerprint = self.get_params('fingerprint').state

        # find the closest
        closest = orders[np.argmin(cdist(np.array(fingerprint, ndmin=2), weights)),:]

        # return a re-sorted egg
        return Egg(pres=[list(pres[idx])], rec=[[None]], features=[list(features[idx])])


    def order(self, egg):
        """
        Reorders a list according to strategy
        """

        def compute_feature_stick(features, weights, alpha):
            '''create a 'stick' of feature weights'''

            feature_stick = []
            for f, w in zip(features, weights):
                feature_stick+=[f]*int(np.power(w,alpha)*100)

            return feature_stick

        def reorder_list(egg, feature_stick, tau):

            def compute_stimulus_stick(s, tau):
                '''create a 'stick' of feature weights'''

                feature_stick = [[weights[feature]]*round(weights[feature]**alpha)*100 for feature in w]
                return [item for sublist in feature_stick for item in sublist]

            # parse egg
            pres, rec, features, dist_funcs = parse_egg(egg)

            # turn pres and features into np arrays
            pres_arr = np.array(pres)
            features_arr = np.array(features)

            # compute distances
            distances = compute_distances(pres, features, dist_funcs)

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
                reordered_features.append(features[next_word_idx])

            return Egg(pres=[reordered_list], rec=[[None]], features=[reordered_features])

        # parse egg
        pres, rec, features, dist_funcs = parse_egg(egg)

        # compute distances
        distances = compute_distances(pres, features, dist_funcs)

        # get params needed for list reordering
        features = self.get_params('fingerprint').get_features()
        weights = self.get_params('fingerprint').state
        alpha = self.get_params('alpha')
        tau = self.get_params('tau')

        # compute feature stick
        feature_stick = compute_feature_stick(features, weights, alpha)

        # reorder list
        return reorder_list(egg, feature_stick, tau)







                # var wordWeights = reorderedList[reorderedList.length - 1].distances[featureStickSample].map(function(distance) {
                #     return distance.dist
                # });

        #         var max = Math.max.apply(null, wordWeights);
        #         wordWeights = wordWeights.map(function(distance) {
        #             if (distance === 0) {
        #                 return distance
        #             } else {
        #                 return distance / max
        #             }
        #         });
        #
        #         var min = Math.min.apply(null, wordWeights.map(function(word) {
        #             return -word
        #         }));
        #
        #         invertedWordWeights = wordWeights.map(function(weight) {
        #                 return -weight - min + .01
        #             })
        #             // console.log('weight', wordWeights)
        #             // console.log('inverted weight', invertedWordWeights)
        #
        #         // create a stick representing the stimuli to chose from
        #         var wordStick = invertedWordWeights.map(function(weight, idx) {
        #             return Array(Math.round(Math.pow(weight, tau) * 100)).fill(idx)
        #         })
        #
        #         wordStick = [].concat.apply([], wordStick);
        #         var wordStickSample = wordStick[_getRandomIntInclusive(0, wordStick.length - 1)]
        #             // console.log('word stick: ', wordStick)
        #             // console.log('word stick sample: ', wordStickSample)
        #             // console.log('chose the word:', nextList[wordStickSample])
        #
        #         // remove the word from the distance object of all stimuli
        #         nextList.forEach(function(stimulus) {
        #             for (feature in stimulus.distances) {
        #                 stimulus.distances[feature].splice(wordStickSample, 1);
        #             }
        #         })
        #         reorderedList.push(nextList[wordStickSample]) // add this stimulus to the reordered list array
        #         nextList.splice(wordStickSample, 1) // remove it from the unordered list
        #     };
        #     // console.log('reordered list: ', reorderedList)
        #     return reorderedList
        # }
        #
        # def stabilize(self, egg):
        #     '''function that returns optimized list'''
        #
        #     # compute average weights
        #     avg_weights = self.get_weights()
        #
        #     # get feature stick
        #     feature_stick = compute_feature_stick(avg_weights, self.alpha)
        #
        #     # return the reordered list
        #     return reorder_list(next_list, feature_stick, self.tau)
        #
        # return next_list

# class Fingerprint(object):
#
#     def __init__(self, state=None, features=None, weights=None, alpha=4, tau=1,
#                  sortby=None, permute=False, nperms=1000):
#
#     def print_params(self):
#       print('state: %s' % self.state)
#       print('features: %s' % self.features)
#       print('weights: %s' % self.weights)
#       print('tau: %d' % self.tau)
#       print('sortby: %s' % self.sortby)
#       print('permute: %d' % self.permute)
#       print('nperms: %d' + self.nperms)
#
#     def get_reordered_list(self, lst):
#
#         print('reordering list according to state %s' % self.state)
#
#         if self.state is 'feature-based':
#             return featurize_list(lst)
#         elif self.state is 'random':
#             return randomize_list(lst)
#         elif self.state is 'optimal':
#             return optimize_list(lst)
#         elif self.state is 'opposite':
#             return oppositize_list(lst)
#         elif self.state is None:
#             print('No fingerprint state assigned.  Returning same list.')
#             return lst
#
#     def get_weights(self):
#         '''function to get the current weights'''
#         return self.weights
#
#     def get_avg_weights(self):
#         '''function to get the current weights'''
#         if self.weights:
#             return map(lambda x: np.mean(x), self.weights)
#
#     def change_state(self, state):
#         '''function to change the fingerprint state'''
#         self.state = state;
#
#     def update_weights(self, weights):
#
#         if self.weights:
#             print('weights exist, updating..')
#             for feature in self.weights:
#                 self.weights[feature].append(weights[feature])
#         else:
#             self.weights = {}
#             for feature in self.weights:
#                 self.weights[feature] = [];
#                 self.weights[feature].append(weights[feature])
#         print('weights updated.')
#
#     def compute_feature_weights(self, pres_list, rec_list, feature_list, distances):
#         """
#         Compute clustering scores along a set of feature dimensions
#
#         Parameters
#         ----------
#         pres_list : list
#             list of presented words
#         rec_list : list
#             list of recalled words
#         feature_list : list
#             list of feature dicts for presented words
#         distances : dict
#             dict of distance matrices for each feature
#
#         Returns
#         ----------
#         weights : list
#             list of clustering scores for each feature dimension
#         """
#
#         # initialize the weights object for just this list
#         weights = {}
#         for feature in feature_list[0]:
#             weights[feature] = []
#
#         # return default list if there is not enough data to compute the fingerprint
#         if len(rec_list) <= 2:
#             print('Not enough recalls to compute fingerprint, returning default fingerprint.. (everything is .5)')
#             for feature in feature_list[0]:
#                 weights[feature] = .5
#             return [weights[key] for key in weights]
#
#         # initialize past word list
#         past_words = []
#         past_idxs = []
#
#         # loop over words
#         for i in range(len(rec_list)-1):
#
#             # grab current word
#             c = rec_list[i]
#
#             # grab the next word
#             n = rec_list[i + 1]
#
#             # if both recalled words are in the encoding list and haven't been recalled before
#             if (c in pres_list and n in pres_list) and (c not in past_words and n not in past_words):
#
#                 # for each feature
#                 for feature in feature_list[0]:
#
#                     # get the distance vector for the current word
#                     dists = distances[feature][pres_list.index(c),:]
#
#                     # distance between current and next word
#                     cdist = dists[pres_list.index(n)]
#
#                     # filter dists removing the words that have already been recalled
#                     dists_filt = np.array([dist for idx, dist in enumerate(dists) if idx not in past_idxs])
#
#                     # get indices
#                     avg_rank = np.mean(np.where(np.sort(dists_filt)[::-1] == cdist)[0]+1)
#
#                     # compute the weight
#                     weights[feature].append(avg_rank / len(dists_filt))
#
#                 # keep track of what has been recalled already
#                 past_idxs.append(pres_list.index(c))
#                 past_words.append(c)
#
#         # average over the cluster scores for a particular dimension
#         for feature in weights:
#             with warnings.catch_warnings():
#                 warnings.simplefilter("ignore", category=RuntimeWarning)
#                 weights[feature] = np.nanmean(weights[feature])
#
#         return [weights[key] for key in weights]
#
#     # private functions
#
#     def default_fingerprint(self):
#         '''return default fingerprint'''
#         return {feature : .5 for feature in self.features}
#
#     def compute_distances(pres_list, feature_list, dist_funcs):
#         """
#         Compute distances between list words along n feature dimensions
#
#         Parameters
#         ----------
#         pres_list : list
#             list of presented words
#         feature_list : list
#             list of feature dicts for presented words
#         dist_funcs : dict
#             dict of distance functions for each feature
#
#         Returns
#         ----------
#         distances : dict
#             dict of distance matrices for each feature
#         """
#
#         # initialize dist dict
#         distances = {}
#
#         # for each feature in dist_funcs
#         for feature in dist_funcs:
#
#             # initialize dist matrix
#             dists = np.zeros((len(pres_list), len(pres_list)))
#
#             # for each word in the list
#             for idx1, item1 in enumerate(pres_list):
#
#                 # for each word in the list
#                 for idx2, item2 in enumerate(pres_list):
#
#                     # compute the distance between word 1 and word 2 along some feature dimension
#                     dists[idx1,idx2] = dist_funcs[feature](feature_list[idx1][feature],feature_list[idx2][feature])
#
#             # set that distance matrix to the value of a dict where the feature name is the key
#             distances[feature] = dists
#
#         return distances
#
#     def recall_matrix(presented, recalled):
#         """
#         Computes recall matrix given list of presented and list of recalled words
#
#         Parameters
#         ----------
#         presented : list of list of strings
#           presentedWords are the words presented in the experiment, in order, grouped by list
#
#         recalled : list of list of strings
#           recalledWords are the words recalled by the subject, in order, grouped by list
#
#         Returns
#         ----------
#         recall_matrix : list of lists of ints
#           each integer represents the presentation position of the recalled word in a given list in order of recall
#           0s represent recalled words not presented
#           negative ints represent words recalled from previous lists
#
#         """
#
#         def recall_pos(pres_list,rec_list):
#             pres_list = list(pres_list)
#             rec_list = list(rec_list)
#             result = np.zeros(len(pres_list)) if len(pres_list)>=len(rec_list) else np.zeros(len(rec_list))
#             result.fill(np.nan)
#             for idx,rec_word in enumerate(rec_list):
#                 if rec_word in pres_list:
#                     if type(rec_word) is str:
#                         result[idx]=int(pres_list.index(rec_word)+1)
#             return result
#
#         result = []
#         for pres_list, rec_list in zip(presented.values, recalled.values):
#             result.append(recall_pos(pres_list, rec_list))
#         return result
#
#
#     def optimize_list(self, next_list):
#         '''function that returns optimized list'''
#
#         # compute average weights
#         avg_weights = self.get_avg_weights()
#
#         # get feature stick
#         feature_stick = compute_feature_stick(avg_weights, self.alpha)
#
#         # return the reordered list
#         return reorder_list(next_list, feature_stick self.tau)
#
#     def oppositize_list(self, next_list):
#         '''function that returns a list opposite of the fingerprint'''
#
#         # compute average weights
#         avg_weights = self.get_avg_weights()
#
#         # invert weights
#         inverted_weights = - (avg_weights - np.mean(avg_weights) - np.min(avg_weights))
#
#         # get feature stick
#         inverted_feature_stick = compute_feature_stick(inverted_weights, self.alpha)
#
#         # return the reordered list
#         return reorder_list(next_list, inverted_feature_stick self.tau)
#
#     def randomize_list(self, next_list):
#         '''function that randomizes a list'''
#
#         return np.random.shuffle(next_list)
#
#     def compute_feature_stick(wts, alpha):
#         '''create a 'stick' of feature weights'''
#
#         feature_stick = [[weights[feature]]*round(weights[feature]**alpha)*100 for feature in wts]
#         return [item for sublist in feature_stick for item in sublist]
#
#
#     def reorder_list(next_list, feature_stick, tau):
#
#         # starting with a random word
#         reordered_list = []
#         reordered_list.append(next_list.pop(np.random.choice(len(next_list), 1)[0]))
#
#         while len(next_list) > 0:
#
#             # sample from the stick
#             feature_sample = feature_stick[np.random.choice(len(feature_stick), 1)[0]]
#
#             # get word weights
#
#             # var wordWeights = reorderedList[reorderedList.length - 1].distances[featureStickSample].map(function(distance) {
#             #     return distance.dist
#             # });
#
#             var max = Math.max.apply(null, wordWeights);
#             wordWeights = wordWeights.map(function(distance) {
#                 if (distance === 0) {
#                     return distance
#                 } else {
#                     return distance / max
#                 }
#             });
#
#             var min = Math.min.apply(null, wordWeights.map(function(word) {
#                 return -word
#             }));
#
#             invertedWordWeights = wordWeights.map(function(weight) {
#                     return -weight - min + .01
#                 })
#                 // console.log('weight', wordWeights)
#                 // console.log('inverted weight', invertedWordWeights)
#
#             // create a stick representing the stimuli to chose from
#             var wordStick = invertedWordWeights.map(function(weight, idx) {
#                 return Array(Math.round(Math.pow(weight, tau) * 100)).fill(idx)
#             })
#
#             wordStick = [].concat.apply([], wordStick);
#             var wordStickSample = wordStick[_getRandomIntInclusive(0, wordStick.length - 1)]
#                 // console.log('word stick: ', wordStick)
#                 // console.log('word stick sample: ', wordStickSample)
#                 // console.log('chose the word:', nextList[wordStickSample])
#
#             // remove the word from the distance object of all stimuli
#             nextList.forEach(function(stimulus) {
#                 for (feature in stimulus.distances) {
#                     stimulus.distances[feature].splice(wordStickSample, 1);
#                 }
#             })
#             reorderedList.push(nextList[wordStickSample]) // add this stimulus to the reordered list array
#             nextList.splice(wordStickSample, 1) // remove it from the unordered list
#         };
#         // console.log('reordered list: ', reorderedList)
#         return reorderedList
#     }
#
#     function _getRandomIntInclusive(min, max) {
#         min = Math.ceil(min);
#         max = Math.floor(max);
#         return Math.floor(Math.random() * (max - min + 1)) + min;
#     };
