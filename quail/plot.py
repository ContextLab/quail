from __future__ import division
import numpy as np
import pandas as pd
import seaborn as sns
from .helpers import *
import matplotlib.pyplot as plt

def plot(data, subjgroup=None, subjname='Subject Group', listgroup=None, listname='List', plot_type=None, plot_style=None, title=None, legend=True, ylim=None, **kwargs):
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

    # convert to tiny and format for plotting
    tidy_data = format2tidy(data, subjname, listname, subjgroup, analysis_type=data.analysis_type)

    #plot!
    if data.analysis_type is 'accuracy':

        # set defaul style to bar
        plot_style = plot_style if plot_style is not None else 'bar'
        plot_type = plot_type if plot_type is not None else 'list'

        if plot_style is 'bar':
            plot_func = sns.barplot
        elif plot_style is 'swarm':
            plot_func = sns.swarmplot
        elif plot_style is 'violin':
            plot_func = sns.violinplot

        if plot_type is 'list':
            ax = plot_func(data=tidy_data, x=listname, y="Accuracy", **kwargs)
        elif plot_type is 'subject':
            ax = plot_func(data=tidy_data, x=subjname, y="Accuracy", **kwargs)
        elif plot_type is 'split':
            ax = plot_func(data=tidy_data, x=subjname, y="Accuracy", hue=listname, **kwargs)

    elif data.analysis_type is 'fingerprint':

        # set default style to violin
        plot_style = plot_style if plot_style is not None else 'violin'
        plot_type = plot_type if plot_type is not None else 'list'

        if plot_style is 'bar':
            plot_func = sns.barplot
        elif plot_style is 'swarm':
            plot_func = sns.swarmplot
        elif plot_style is 'violin':
            plot_func = sns.violinplot


        if plot_type is 'list':
            ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", hue=listname, **kwargs)
        elif plot_type is 'subject':
            ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", hue=subjname, **kwargs)
        else:
            ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", **kwargs)

    elif data.analysis_type is 'spc':

        plot_type = plot_type if plot_type is not None else 'list'

        if plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Proportion Recalled", unit="Subject", condition=subjname, **kwargs)
        elif plot_type is 'list':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Proportion Recalled", unit="Subject", condition=listname, **kwargs)
        ax.set_xlim(0,data.list_length)

    elif data.analysis_type is 'pfr':

        plot_type = plot_type if plot_type is not None else 'list'

        if plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Probability of First Recall", unit="Subject", condition=subjname, **kwargs)
        elif plot_type is 'list':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Probability of First Recall", unit="Subject", condition=listname, **kwargs)
        ax.set_xlim(0,data.list_length)

    if data.analysis_type=='lagcrp':

        plot_type = plot_type if plot_type is not None else 'list'

        if plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Conditional Response Probability", unit="Subject", condition=subjname, **kwargs)
        elif plot_type is 'list':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Conditional Response Probability", unit="Subject", condition=listname, **kwargs)
        ax.set_xlim(-5,5)

    # add title
    if title:
        plt.title(title)

    if legend is False:
        try:
            ax.legend_.remove()
        except:
            pass

    if ylim:
        plt.ylim(ylim)

    plt.show()

    return ax
