



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