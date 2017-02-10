
# coding: utf-8

# <h1>Pyrororobocop</h1>

# In[1]:

import pandas as pd
from analysis import recall_matrix

class Pyro(object):
    """
    Data object for the pyrec package

    This class contains free recall data and metadata that will be used by pyrec.

    Attributes
    ----------
    
    pres : pd.DataFrame
        Dataframe containing the presented words.  Each row represents the presented words for a given list and each column
        represents a list. The cells should be lowercase words. The index will be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number
    
    features : pd.DataFrame
        Dataframe containing the features for presented words.  Each row represents the presented words for a given list and each column
        represents a list. The cells should be a dictionary of features, where the keys are the name of the features, and the values are the feature values.
        The index will be a multi-index, where the first level reprensents the subject number and the second level represents the list number
        
    rec : pd.DataFrame
        Dataframe containing the words recalled.  Each row represents the recalled words for a given list and each column
        represents a list.  Each row represents the recalled words for a given list and each column
        represents a list. The cells should be lowercase words. The index will be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number
    
    meta : dict (optional)
        Meta data about the study (i.e. version, description, date, etc.) can be saved here
    
    """


    def __init__(self, pres=pd.DataFrame(), features=pd.DataFrame(), rec=pd.DataFrame(), meta={}):

        self.pres=pres
        self.features=features
        self.rec=rec
        self.meta=meta
        self._recall_mtx = recall_matrix(self.pres, self.rec)



# In[2]:

Pyro()


# In[3]:

from sqlalchemy import create_engine, MetaData, Table
import json
import pandas as pd
import numpy as np
import math
from __future__ import division
import re
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import numpy.ma as ma
from itertools import izip_longest
from collections import Counter


# <h1> Load data in dataframe</h1>

# In[4]:

db_url = "sqlite:///participants.db"
table_name = 'turkdemo'
data_column_name = 'datastring'

# boilerplace sqlalchemy setup
engine = create_engine(db_url)
metadata = MetaData()
metadata.bind = engine
table = Table(table_name, metadata, autoload=True)

# make a query and loop through
s = table.select()
rows = s.execute()

data = []
for row in rows:
    data.append(row[data_column_name])
    
# Now we have all participant datastrings in a list.
# Let's make it a bit easier to work with:

# parse each participant's datastring as json object
# and take the 'data' sub-object
data = [json.loads(part)['data'] for part in data if part is not None]

# insert uniqueid field into trialdata in case it wasn't added
# in experiment:
for part in data:
    for record in part:
#         print(record)
        if type(record['trialdata']) is list:

            record['trialdata'] = {record['trialdata'][0]:record['trialdata'][1]}
        record['trialdata']['uniqueid'] = record['uniqueid']
        
# flatten nested list so we just have a list of the trialdata recorded
# each time psiturk.recordTrialData(trialdata) was called.
def isNotNumber(s):
    try:
        float(s)
        return False
    except ValueError:
        return True

data = [record['trialdata'] for part in data for record in part]

# filter out fields that we dont want using isNotNumber function
filtered_data = [{k:v for (k,v) in part.items() if isNotNumber(k)} for part in data]
    
# Put all subjects' trial data into a dataframe object from the
# 'pandas' python library: one option among many for analysis
data_frame = pd.DataFrame(filtered_data)


# <h1> Track Experiement Number</h1>

# In[5]:

db_url = "sqlite:///participants.db"
table_name = 'turkdemo'
data_column_name = 'codeversion'

# boilerplace sqlalchemy setup
engine = create_engine(db_url)
metadata = MetaData()
metadata.bind = engine
table = Table(table_name, metadata, autoload=True)

# make a query and loop through
s = table.select()
rows = s.execute()

versions = []
for row in rows:
    versions.append(row[data_column_name])
    
version_col = []
for idx,sub in enumerate(data_frame['uniqueid'].unique()):
    for i in range(sum(data_frame['uniqueid']==sub)):
        version_col.append(versions[idx])
data_frame['exp_version']=version_col


# <h1>Word Pool</h1>

# In[6]:

# read in stimulus library
wordpool = pd.read_csv('cut_wordpool.csv')


# <h1>Select Experiment</h1>

# In[7]:

subids = list(data_frame[data_frame['listNumber']==15]['uniqueid'].unique())

d = dict()
for sub in subids:
    key = data_frame[data_frame['uniqueid']==sub]['exp_version'].values[0]
    if key in d:
        d[key].append(sub)
    else:
        d[key]=[sub]

#reaplce these values with the experiment number
#three values for the case of experiment 1 only
#print (d["0.0"], d['1.0'], d['1.1'])

exp1=d["0.0"]+d['1.0']+d['1.1']


exp1.remove('debugGPNALW:debugXSJ1FD')
exp1.remove('debugLXMXTP:debugJAXRZL')
exp1.remove('debugHP65NS:debugLWS9KB')
exp1.remove('debugKUWU41:debug9FG9EP')


# subids.remove('debug4PXFJG:debug3V9BT9')
# subids.remove('debugAD2211:debugB3TKJQ')
# subids.remove('debug7XDZDR:debugO8OCCV') # all of the audio files are empty ?!
# subids.remove('debugTX7U35:debugZFTPLT')
##################

print(exp1)


# <h1>Processing Functions</h1>

# In[8]:

# this function takes the data frame and returns subject specific data based on the subid variable
def filterData(data_frame,subid):
    filtered_stim_data = data_frame[data_frame['stimulus'].notnull() & data_frame['listNumber'].notnull()]
    filtered_stim_data = filtered_stim_data[filtered_stim_data['trial_type']=='single-stim']
    filtered_stim_data =  filtered_stim_data[filtered_stim_data['uniqueid']==subid]
    return filtered_stim_data

# this function parses the data creating an array of dictionaries, where each dictionary represents a trial (word presented) along with the stimulus attributes
def createStimDict(data):
    stimDict = []
    for index, row in data.iterrows():
        stimDict.append({
                'text': str(re.findall('>(.+)<',row['stimulus'])[0]),
                'color' : { 'r' : int(re.findall('rgb\((.+)\)',row['stimulus'])[0].split(',')[0]),
                           'g' : int(re.findall('rgb\((.+)\)',row['stimulus'])[0].split(',')[1]),
                           'b' : int(re.findall('rgb\((.+)\)',row['stimulus'])[0].split(',')[2])
                           },
                'location' : {
                    'top': float(re.findall('top:(.+)\%;', row['stimulus'])[0]),
                    'left' : float(re.findall('left:(.+)\%', row['stimulus'])[0])
                    },
                'category' : wordpool['CATEGORY'].iloc[list(wordpool['WORD'].values).index(str(re.findall('>(.+)<',row['stimulus'])[0]))],
                'size' : wordpool['SIZE'].iloc[list(wordpool['WORD'].values).index(str(re.findall('>(.+)<',row['stimulus'])[0]))],
                'wordLength' : len(str(re.findall('>(.+)<',row['stimulus'])[0])),
                'firstLetter' : str(re.findall('>(.+)<',row['stimulus'])[0])[0],
                'listnum' : row['listNumber']
            })
    return stimDict

# this function loads in the recall data into an array of arrays, where each array represents a list of words
def loadRecallData(subid):
    recalledWords = []
    for i in range(0,16):
        try:
            f = open('recall_data/' + subid + '-' + str(i) + '.wav.txt', 'rb')
            try:
                spamreader = csv.reader(f, delimiter=' ', quotechar='|')
            except:
                f = open('recall_data/' + subid + '/' + subid + '-' + str(i) + '.wav.txt', 'rb')
                spamreader = csv.reader(f, delimiter=' ', quotechar='|')
        except (IOError, OSError) as e:
            print(e)
        for row in spamreader:
            recalledWords.append(row[0].split(','))
    return recalledWords

# this function computes accuracy for a series of lists
def computeListAcc(stimDict,recalledWords):
    accVec = []
    for i in range(0,16):
        stim = [stim['text'] for stim in stimDict if stim['listnum']==i]
        recalled= recalledWords[i]
        
        acc = 0
        tmpstim = stim[:]
        for word in recalled:
            if word in tmpstim:
                tmpstim.remove(word)
                acc+=1
        accVec.append(acc/len(stim))
    return accVec


# <h1>Create presentedWords and recalledWords</h1>

# In[9]:

experiment=[]
all_recalled=[]
all_presented=[]
for idx,sub in enumerate(exp1):

    filteredStimData = filterData(data_frame,sub)
    stimDict = createStimDict(filteredStimData)
    #get and parse subject's data

    presentedWords = [[] for i in range(0,16)]  
    for data in stimDict:
        presentedWords[int(data['listnum'])].append(data['text'])

    recalledWords = loadRecallData(sub)
    experiment.append(recall_matrix(presentedWords, recalledWords))
    
    all_recalled.append(recalledWords)
    all_presented.append(presentedWords)
    
print(len(all_presented))
print(all_presented)


# <h1>Create Presented DataFrame</h1>

# In[39]:

def pres2pd(all_presented):
    
    def indexing(all_presented):
    
        subs = len(all_presented)

        subs_idx = []
        lsts_idx = []
        for idx,subs in enumerate(all_presented):

            for idx2,sub in enumerate(subs):
                sub_idx = []
                lst_idx = []

                for idx3,lst in enumerate(sub):
                    lst_idx.append(idx3)

                sub_idx = [idx2]*len(lst_idx)

                subs_idx.append(sub_idx)
                lsts_idx.append(lst_idx)

        subs_index = [item for sublist in subs_idx for item in sublist]
        lsts_index = [item for sublist in lsts_idx for item in sublist]
        
        return(subs_index, lsts_index)
    
    #####################
    
    #Make dataframe
    longest = len(max(all_presented,key=len))
    index = [indexing(all_presented)[0],indexing(all_presented)[1]]
    columns = list(range(0,longest))
    all_lists = [item for sublist in all_presented for item in sublist]
    
    ###FIRST ATTEMPTS 
    df = pd.DataFrame(index = index, columns = columns)
    
    for indx,subject in enumerate(all_presented):
        for idx,lst in enumerate(subject):
            #for x in range(0, len(lst)):
            df.iloc[indx][idx] = lst[idx]
    
    return(df)

    ###SUGGESTED
#     for sub in all_presented:
#         subs_list_of_dfs = [pd.DataFrame (lst) for lst in sub]
#         subs_df = pd.concat(subs_list_of_dfs)
    
#     return(subs_df)
    
    
tester = pres2pd(all_presented)
tester

            


# In[207]:

import pandas as pd
subs = [[["apple", "banana"], ["carrot", "cucumber", "orange"]],[["ant", "bag"], ["celery", "parsnip", "pear"]]]
subs_list_of_dfs = [pd.DataFrame (sub) for sub in subs]
subs_df = pd.concat(subs_list_of_dfs)
subs_df


# In[ ]:


