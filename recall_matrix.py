def recall_matrix(presentedWords, recalledWords):
    """
    input1: presentedWords- list of lists, in order of presentation
    input2: recalledWords- list of lists, in order of recall
    output: list of lists, recall matrix
    
    note: recalled word from previous list --> negative value
    note: recalled word not presented --> zero
    note: nothing at this time for recalled words that will appear on later lists
    """

    recall_matrix=[[] for i in range(0,len(presentedWords))]
    
    for idx,wordList in enumerate(recalledWords):
        for word in wordList:
            if word in presentedWords[idx]:
                recall_matrix[idx].append(presentedWords[idx].index(word)+1)
            #if the recalled word was presented, add to the recall matrix its presentation position
                
            elif not word in presentedWords[idx]:
                for z in range(0,idx):
                    if word in presentedWords[z]:
                        if idx-z < 0:
                            recall_matrix[idx].append(z-idx)

                        #puts a negative number for word recalled from previous list
                        #at present, nothing for words from future lists 
                else:
                    recall_matrix[idx].append(0)       
            #if recalled word was not presented, append zero
            
    return recall_matrix