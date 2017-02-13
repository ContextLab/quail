import numpy as np
import matplotlib.pyplot as plt

def serialPos(recall_matrix,num,plot=True):

    """
    input 1: recall_matrix
    input 2: number of words presented in each list
    optional: plot=True/False

    output (plot=True): plot of probability of a word being recalled given presentation position
    output (plot=False): list of probabilities

    """
    
    recalled=np.zeros((len(recall_matrix),num),dtype=np.int)
    #empty array, one row per trial, one column for each presented word
    
    for idx,trial in enumerate(recall_matrix):
        #for each trial in recall matrix
        for position in range(1,num+1):
            #for each position number (1 indexed)
            if position in trial:
                recalled[idx][position-1]=1
            else:
                recalled[idx][position-1]=0
            #if that position was recllaed in a given trial, add 1 to that position in the appropriate row of recalled
            #else, add zero
            #this ignores negative numbers (words from previous lists) and zeros (words not presented) 
                
    prob=np.mean(recalled, axis=0)
    #take the mean of each column

    if plot==True:
        plt.plot(range(1,len(prob)+1),prob,color='black')
    
    else:
        return prob