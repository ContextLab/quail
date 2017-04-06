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
    data : pyro data object
        The data to be analyzed

    subjgroup : list of strings or ints
        String/int variables indicating how to group over subjects.  Must be
        the length of the number of subjects

    listgroup : list of strings or ints
        String/int variables indicating how to group over list.  Must be
        the length of the number of lists

    analysis : function
        This function analyzes data and returns it

    Returns
    ----------
    analyzed_data : pyro data object
        Pyro containing the analysis results

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
    tidy_data = format2tidy(averaged_data, analysis_type=data.analysis_type)

    #plot!
    if data.analysis_type is 'accuracy':

        plot_style = plot_style if plot_style is not None else 'bar'
        # plot_type = plot_type if plot_type is not None else 'subject'

        if plot_style is 'bar':
            if plot_type is 'list':
                ax = sns.barplot(data=tidy_data, x="List", y="Accuracy", hue="List", **kwargs)
            elif plot_type is 'subject':
                ax = sns.barplot(data=tidy_data, x="Subject", y="Accuracy", hue="Subject", **kwargs)
            else:
                ax = sns.barplot(data=tidy_data, y="Accuracy", **kwargs)
        elif plot_style is 'swarm':
            if plot_type is 'list':
                ax = sns.swarmplot(data=tidy_data, x="List", y="Accuracy", hue="List", **kwargs)
            elif plot_type is 'subject':
                ax = sns.swarmplot(data=tidy_data, x="Subject", y="Accuracy", hue="Subject", **kwargs)
            else:
                ax = sns.swarmplot(data=tidy_data, y="Accuracy", **kwargs)
        elif plot_style is 'violin':
            if plot_type is 'list':
                ax = sns.violinplot(data=tidy_data, x="List", y="Accuracy", hue="List", **kwargs)
            elif plot_type is 'subject':
                ax = sns.violinplot(data=tidy_data, x="Subject", y="Accuracy", hue="Subject", **kwargs)
            else:
                ax = sns.violinplot(data=tidy_data, y="Accuracy", **kwargs)

    elif data.analysis_type is 'fingerprint':
        if plot_type is 'bar':
            if hue is 'list':
                ax = sns.barplot(data=tidy_data, x="Feature", y="Value", hue="List", **kwargs)
            elif hue is 'subject':
                ax = sns.barplot(data=tidy_data, x="Feature", y="Value", hue="Subject", **kwargs)
            else:
                ax = sns.barplot(data=tidy_data, x="Feature", y="Value", **kwargs)
        elif plot_type is 'swarm':
            if hue is 'list':
                ax = sns.swarmplot(data=tidy_data, x="Feature", y="Value", hue="List", **kwargs)
            elif hue is 'subject':
                ax = sns.swarmplot(data=tidy_data, x="Feature", y="Value", hue="Subject", **kwargs)
            else:
                ax = sns.swarmplot(data=tidy_data, x="Feature", y="Value", **kwargs)
        else:
            if hue is 'list':
                ax = sns.violinplot(data=tidy_data, x="Feature", y="Value", hue="List", **kwargs)
            elif hue is 'subject':
                ax = sns.violinplot(data=tidy_data, x="Feature", y="Value", hue="Subject", **kwargs)
            else:
                ax = sns.violinplot(data=tidy_data, x="Feature", y="Value", **kwargs)
        ax.set_ylim(0,1)
    else:
        if plot_type is 'grid':
            ax = sns.FacetGrid(tidy_data, row="Subject", col="List")
            ax = ax.map(sns.tsplot, "Value")
        elif plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Value", unit="List", condition="Subject", **kwargs)
        else:
            ax = sns.tsplot(data = tidy_data, time="Position", value="Value", unit="Subject", condition="List", **kwargs)

    if data.analysis_type=='lagcrp':
        ax.set_xlim(-5,5)
    elif data.analysis_type in ['spc','pfr','plr']:
        ax.set_xlim(0,data.list_length)

    plt.show()

    return ax
