# -*- coding: utf-8 -*-
import math
import numpy as np

# given a stimulus list and recalled words, compute the weights
def get_fingerprint(current_list, recalled_words):
    current_list = compute_distance(current_list)
    return compute_feature_weights(current_list, recalled_words, features)

#### private functions ####

def compute_distance(stim_array):

    # initialize distance dictionary
    for stimulus in stim_array:
        stimulus['distances'] = {}
        for feature in features:
            stimulus['distances'][feature] = []

    # loop over the lists to create distance matrices
    for i,stimulus1 in enumerate(stim_array):
        for j,stimulus2 in enumerate(stim_array):

            stim_array[i]['distances'][feature].append({
                    'word' : stim_array[j]['text'],
                    'dist' : dist_funcs[featuren](stim_array[i][feature],stim_array[j][feature])
                })

    return stim_array

def compute_feature_weights(current_list, recalled_words, features):

    # initialize the weights object for just this list
    listWeights = {}
    for feature in features:
        listWeights[feature] = []

    # return default list if there is not enough data to compute the fingerprint
    if len(recalled_words) <= 2:
        print('Not enough recalls to compute fingerprint, returning default fingerprint.. (everything is .5)')
        for feature in features:
            listWeights[feature] = .5
        return listWeights

    # initialize pastWords list
    pastWords = []

    # finger print analysis
    for i in range(0,len(recalled_words)-1):

        # grab current word
        currentWord = recalled_words[i]

        # grab the next word
        nextWord = recalled_words[i + 1]

        # grab the words from the encoding list
        encodingWords = [stimulus['text'] for stimulus in current_list]

        # append current word to past words log
        # pastWords.append(currentWord)

        # if both recalled words are in the encoding list
        if (currentWord in encodingWords and nextWord in encodingWords) and (currentWord not in pastWords and nextWord not in pastWords):
            # print(currentWord,nextWord,encodingWords,pastWords)

            for feature in features:

                # get the distance vector for the current word
                distVec = current_list[encodingWords.index(currentWord)]['distances'][feature]

                # filter distVec removing the words that have already been analyzed from future calculations
                filteredDistVec = []
                for word in distVec:
                    if word['word'] in pastWords:
                        pass
                    else:
                        filteredDistVec.append(word)

                # sort distWords by distances
                filteredDistVec = sorted(filteredDistVec, key=lambda item:item['dist'])

                # compute the category listWeights
                nextWordIdx = [word['word'] for word in filteredDistVec].index(nextWord)

                # not sure about this part
                idxs = []
                for idx,word in enumerate(filteredDistVec):
                    if filteredDistVec[nextWordIdx]['dist'] == word['dist']:
                        idxs.append(idx)

                listWeights[feature].append(1 - (sum(idxs)/len(idxs) / len(filteredDistVec)))

            pastWords.append(currentWord)

    for feature in listWeights:
        listWeights[feature] = np.mean(listWeights[feature])

    return listWeights
