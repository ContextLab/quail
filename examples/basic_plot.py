#import
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#data
pos = np.arange(0,8)
subj = np.zeros(8)
value = np.arange(0,8)
df = pd.DataFrame(np.array([subj,pos,value]).T, columns=['Subject', 'Position', 'Value'])

#plot
ax = sns.tsplot(data = df, time = "Position", value="Value", unit="Subject")
plt.show()
