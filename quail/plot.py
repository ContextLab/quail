from __future__ import division
import numpy as np
import pandas as pd
import seaborn as sns
from .helpers import *
import matplotlib.pyplot as plt

def plot(data, subjgroup=None, subjname='Subject', listgroup=None, listname='List', plot_type=None, plot_style=None, **kwargs):
    """
    General plot function that groups data by subject/list number and performs analysis.

    Parameters
    ----------
    data : egg data object
        The data to be analyzed

    subjgroup : list of strings or ints
        String/int variables indicating how to group over subjects.  Must be
        the length of the number of subjects

    listgroup : list of strings or ints
        String/int variables indicating how to group over list.  Must be
        the length of the number of lists


    Returns
    ----------
    analyzed_data : egg data object
        Egg containing the analysis results

    """

    # if no grouping, set default to iterate over each list independently
    subjgroup = subjgroup if subjgroup else data.index.levels[0].values
    listgroup = listgroup if listgroup else data.index.levels[1].values

    # create a dictionary for grouping
    subjdict = {subj : data.index.levels[0].values[subj==np.array(subjgroup)] for subj in set(subjgroup)}
    listdict = {lst : data.index.levels[1].values[lst==np.array(listgroup)] for lst in set(listgroup)}

    # perform the analysis
    averaged_data = []
    for subj in subjdict:
        for lst in listdict:

            # get data slice for presentation and recall
            data_slice = data.loc[[(s,l) for s in subjdict[subj] for l in listdict[lst]]]

            # generate index
            index = pd.MultiIndex.from_arrays([[subj],[lst]], names=[subjname, listname])

            # perform analysis for each data chunk
            if data.analysis_type is 'fingerprint':
                averaged = pd.DataFrame([np.mean(data_slice.values, axis=0)], index=index, columns=data_slice.columns)
            else:
                averaged = pd.DataFrame([np.mean(data_slice.values, axis=0)], index=index)

            # append analyzed data
            averaged_data.append(averaged)

    # concatenate slices
    averaged_data = pd.concat(averaged_data)

    # convert to tiny and format for plotting
    tidy_data = format2tidy(averaged_data, subjname, listname, analysis_type=data.analysis_type)

    #plot!
    if data.analysis_type is 'accuracy':

        # set defaul style to bar
        plot_style = plot_style if plot_style is not None else 'bar'

        if plot_style is 'bar':
            if plot_type is 'list':
                ax = sns.barplot(data=tidy_data, x=listname, y="Accuracy", hue=listname, **kwargs)
            elif plot_type is 'subject':
                ax = sns.barplot(data=tidy_data, x=subjname, y="Accuracy", hue=subjname, **kwargs)
            else:
                ax = sns.barplot(data=tidy_data, y="Accuracy", **kwargs)
        elif plot_style is 'swarm':
            if plot_type is 'list':
                ax = sns.swarmplot(data=tidy_data, x=listname, y="Accuracy", hue=listname, **kwargs)
            elif plot_type is 'subject':
                ax = sns.swarmplot(data=tidy_data, x=subjname, y="Accuracy", hue=subjname, **kwargs)
            else:
                ax = sns.swarmplot(data=tidy_data, y="Accuracy", **kwargs)
        elif plot_style is 'violin':
            if plot_type is 'list':
                ax = sns.violinplot(data=tidy_data, x=listname, y="Accuracy", hue=listname, **kwargs)
            elif plot_type is 'subject':
                ax = sns.violinplot(data=tidy_data, x=subjname, y="Accuracy", hue=subjname, **kwargs)
            else:
                ax = sns.violinplot(data=tidy_data, y="Accuracy", **kwargs)

    elif data.analysis_type is 'fingerprint':

        # set defaul style to violin
        plot_style = plot_style if plot_style is not None else 'violin'

        if plot_style is 'bar':
            if plot_type is 'list':
                ax = sns.barplot(data=tidy_data, x="Feature", y="Clustering Score", hue=listname, **kwargs)
            elif plot_type is 'subject':
                ax = sns.barplot(data=tidy_data, x="Feature", y="Clustering Score", hue=subjname, **kwargs)
            else:
                ax = sns.barplot(data=tidy_data, x="Feature", y="Clustering Score", **kwargs)
        elif plot_style is 'swarm':
            if plot_type is 'list':
                ax = sns.swarmplot(data=tidy_data, x="Feature", y="Clustering Score", hue=listname, **kwargs)
            elif plot_type is 'subject':
                ax = sns.swarmplot(data=tidy_data, x="Feature", y="Clustering Score", hue=subjname, **kwargs)
            else:
                ax = sns.swarmplot(data=tidy_data, x="Feature", y="Clustering Score", **kwargs)
        else:
            if plot_type is 'list':
                ax = sns.violinplot(data=tidy_data, x="Feature", y="Clustering Score", hue=listname, **kwargs)
            elif plot_type is 'subject':
                ax = sns.violinplot(data=tidy_data, x="Feature", y="Clustering Score", hue=subjname, **kwargs)
            else:
                ax = sns.violinplot(data=tidy_data, x="Feature", y="Clustering Score", **kwargs)
        ax.set_ylim(0,1)

    elif data.analysis_type is 'spc':
        if plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Proportion Recalled", unit=listname, condition=subjname, **kwargs)
        else:
            ax = sns.tsplot(data = tidy_data, time="Position", value="Proportion Recalled", unit=subjname, condition=listname, **kwargs)
        ax.set_xlim(0,data.list_length)

    elif data.analysis_type is 'pfr':
        if plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Probability of First Recall", unit=listname, condition=subjname, **kwargs)
        else:
            ax = sns.tsplot(data = tidy_data, time="Position", value="Probability of First Recall", unit=subjname, condition=listname, **kwargs)
        ax.set_xlim(0,data.list_length)

    if data.analysis_type=='lagcrp':
        if plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Conditional Response Probability", unit=listname, condition=subjname, **kwargs)
        else:
            ax = sns.tsplot(data = tidy_data, time="Position", value="Conditional Response Probability", unit=subjname, condition=listname, **kwargs)
        ax.set_xlim(-5,5)

    plt.show()

    return ax
