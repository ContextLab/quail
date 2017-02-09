#!/usr/bin/env python

from __future__ import division
import numpy as np
import pandas as pd

##RECALL MATRIX#######

def recall_matrix(presented, recalled):
    """
    Computes recall matrix given list of presented and list of recalled words

    Parameters
    ----------
    presented : list of list of strings
      presentedWords are the words presented in the experiment, in order, grouped by list
    
    recalled : list of list of strings
      recalledWords are the words recalled by the subject, in order, grouped by list
    
    Returns
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists
    
    """

    recall_matrix=[[] for i in range(0,len(presented))]
    
    for idx,wordList in enumerate(recalled):
        for word in wordList:
            if word in presented[idx]:
                recall_matrix[idx].append(presented[idx].index(word)+1)
                #if the recalled word was presented, add to the recall matrix its presentation position
                
            elif not word in presented[idx]:
                for z in range(0,idx):
                    if word in presented[z]:
                        recall_matrix[idx].append(z-idx)
                        #note, verify that by using [idx] here, we prevent positive value for "future" word
                        #puts a negative number for word recalled from previous list
                else:
                    recall_matrix[idx].append(np.nan)       
            #if recalled word was not presented, append zero
            
    return recall_matrix

def serial_pos(recall_matrix):
    """
    Computes probability of a word being recalled (in the appropriate recall list), given its presentation position 

    Parameters
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists  
    
    Returns
    ----------
    probabilities : numpy array of ints
      each int represents the probability of recall for a word presented in given position/index 
      
    """

    recalled=np.zeros((len(recall_matrix),len(recall_matrix[0])),dtype=np.int)
    #empty array, one row per trial, one column for each presented word
    
    for idx,trial in enumerate(recall_matrix):
        #for each trial in recall matrix
        for position in range(1,len(recall_matrix[0])+1):
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

    return prob

#PROB FIRST RECALL######

def pfr(recall_matrix):

    """
    Computes probability of a word being recalled first (in the appropriate recall list), given its presentation position 

    Parameters
    ----------
    recall_matrix : list of lists of ints
      each integer represents the presentation position of the recalled word in a given list in order of recall
      0s represent recalled words not presented
      negative ints represent words recalled from previous lists  
    
    Returns
    ----------
    probabilities : numpy array of ints
      each int represents the probability of first recall for a word presented in given position/index 
      
    """

    recalled=np.zeros((len(recall_matrix),len(recall_matrix[0])),dtype=np.int)
    #empty array, one row per trial, one column for each presented word
    for idx,trial in enumerate(recall_matrix):
        #for each trial in recall matrix
        for position in range(1,len(recall_matrix[0])+1):
            #for each possible position (1 indexed)
            if trial[0]==position:
                #if that position is first in the given trial
                recalled[idx][position-1]=1
                #append recalled appropriate row and position
                
    prob=np.mean(recalled, axis=0)
    return prob


#PROB LAST RECALL#######

##NOTES: 

def plr(recall_matrix):
    recalled=np.zeros((len(recall_matrix),len(recall_matrix[0])),dtype=np.int)
    #empty array, one row per trial, one column for each presented word
    for idx,trial in enumerate(recall_matrix):
        #for each trial in recall matrix
        
        z=trial[-1]
        while (type(z)==float or z<=0):
            new=trial.index(z)-1
            z=trial[new]
            print(z)
    
        ##what if entire recall matrix is nans? 
        #(subject recalls no words)
        
        if z in range(1,len(recall_matrix[0])+1):
            recalled[idx][z-1]+=1
             
    prob=np.mean(recalled, axis=0)

    return prob 

def crp(recall_matrix):
    
    def check_pair(a, b):
        if (a>0 and b>0) and (a!=b):
            return True
        else:
            return False

    def compute_actual(recall_list):
        length=len(recall_list)
        arr=pd.Series(data=np.zeros((length-1)*2), index=list(range(1-length,0))+list(range(1,length)))
        recalled=[]
        for trial in range(0,length-1):
            a=recall_list[trial]
            b=recall_list[trial+1]
            if check_pair(a, b) and (a not in recalled) and (b not in recalled):
                arr[b-a]+=1
            recalled.append(a)
        return arr
                      
    def compute_possible(recall_list):
        length=len(recall_list)
        arr=pd.Series(data=np.zeros((length-1)*2), index=list(range(1-length,0))+list(range(1,length)))
                      
        recalled=[]
        for trial in recall_list:    
                      
            low_bound=1-trial
            up_bound=length-trial

            chances=range(low_bound,0)+range(1,up_bound+1)
            #ALL transitions
            
                      
            #remove transitions not possible
            for each in recalled:
                chances.remove(each-trial)
                      
            
            #update array with possible transitions        
            arr[chances]+=1       
                      
            recalled.append(trial)
            
        return arr
                      
    ########                 
      
    list_crp = []
    for n_list in recall_matrix:
        actual = compute_actual(n_list)
        possible = compute_possible(n_list)
               
        list_crp.append([0.0 if i==0 and j==0 else i/j for i,j in zip(actual,possible)])
        #if actual and possible are both zero, append zero; otherwise, divide  
        
    return list_crp   
