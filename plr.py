import numpy as np
import matplotlib.pyplot as plt


def plr(recall_matrix,num,plot=True):
    recalled=np.zeros((len(recall_matrix),num),dtype=np.int)
    #empty array, one row per trial, one column for each presented word
    for idx,trial in enumerate(recall_matrix):
        #for each trial in recall matrix
        for position in range(1,num+1):
            #for each possible presentation position, excluding zeros and negatives
            if trial[-1]==position:
                recalled[idx][position-1]=1
                #if the last word recalled is in a given position, append a 1 to the corresponding position in recalled
        
    prob=np.mean(recalled, axis=0)

    if plot==True:
        plt.plot(range(1,len(prob)+1),prob,color='black', lw=1)
    
    else:
        return prob  