import numpy as np
import matplotlib.pyplot as plt

def pfr(recall_matrix,num,plot=True):


    recalled=np.zeros((len(recall_matrix),num),dtype=np.int)
    #empty array, one row per trial, one column for each presented word
    for idx,trial in enumerate(recall_matrix):
        #for each trial in recall matrix
        for position in range(1,num+1):
            #for each possible position (1 indexed)
            if trial[1]==position:
                #if that position is first in the given trial
                recalled[idx][position-1]=1
                #append recalled appropriate row and position
                
    prob=np.mean(recalled, axis=0)

    if plot==True:
        plt.plot(range(1,len(prob)+1),prob,color='tan', lw=1)
    
    else:
        return prob