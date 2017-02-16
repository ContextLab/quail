import pandas as pd

def list2pd(all_data):
    """
    Makes multi-indexed dataframe of subject data 

    Parameters
    ----------
    all_data : list of lists of strings
        strings are either all presented or all recalled items, in the order of presentation or recall 
        *should also work for presented / recalled ints and floats, if desired
        

    Returns
    ----------
    subs_list_of_dfs : multi-indexed dataframe 
        dataframe of subject data (presented or recalled words/items), indexed by subject and list number
        cell populated by the term presented or recalled in the position indicated by the column number

    """
    
    
    def make_multi_index(sub_data, isub):
        return pd.MultiIndex.from_tuples([(sub_num,lst_num) for lst_num,lst in enumerate(sub_data)], names = ['Subject', 'List'])
    
    subs_list_of_dfs = [pd.DataFrame(sub_data, index=make_multi_index(sub_data, sub_num)) for sub_num,sub_data in enumerate(all_data)]
    return pd.concat(subs_list_of_dfs)

