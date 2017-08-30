#!/usr/bin/env python
import numpy as np

class Fingerprint(object):

    def __init__(self, features=None, state=None, n=0, permute=False, nperms=1000):

        if state is None:
            self.state = {feature : [.5] for feature in features}

    def update(self, pres_list, rec_list, feature_list, dist_funcs):
        """
        Updates fingerprint with new data

        Parameters
        ----------
        pres_list : list
            list of presented words
        rec_list : list
            list of recalled words
        feature_list : list
            list of feature dicts for presented words
        dist_funcs : dict
            dict of distance functions for each feature

        Returns
        ----------
        None
        """

        # compute weights for a single list
        next_weights = compute_feature_weights(pres_list, rec_list, feature_list, dist_funcs)

        # increment n
        self.n+=1

        # multiply states by n
        c = self.state*n

        # update state
        self.state = (c+next_weights)/(self.n+1)

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

class OptimalPresenter(object):

    def __init__(self, strategy='random', features=None, params=None,
                 fingerprint=None):

        if params is None:
            self.params = {'alpha' : 4, 'tau' : 1}

        if fingerprint is None:
            self.fingerprint = Fingerprint()

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

    def order(self, next_list):
        """
        Reorders a list according to strategy
        """

        def get_feature_stick(w, alpha):
            '''create a 'stick' of feature weights'''

            feature_stick = [[weights[feature]]*round(weights[feature]**alpha)*100 for feature in w]
            return [item for sublist in feature_stick for item in sublist]

        def compute_stimulus_stick(s, tau):
            '''create a 'stick' of feature weights'''

            feature_stick = [[weights[feature]]*round(weights[feature]**alpha)*100 for feature in w]
            return [item for sublist in feature_stick for item in sublist]


        return next_list

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
