from __future__ import division
import numpy as np
import pandas as pd
import seaborn as sns
from .helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42

def plot(results, subjgroup=None, subjname='Subject Group', listgroup=None,
         listname='List', subjconds=None, listconds=None, plot_type=None,
         plot_style=None, title=None, legend=True, xlim=None, ylim=None, save_path=None,
         **kwargs):
    """
    General plot function that groups data by subject/list number and performs analysis.

    Parameters
    ----------
    results : quail.FriedEgg
        Object containing results

    subjgroup : list of strings or ints
        String/int variables indicating how to group over subjects.  Must be
        the length of the number of subjects

    subjname : string
        Name of the subject grouping variable

    listgroup : list of strings or ints
        String/int variables indicating how to group over list.  Must be
        the length of the number of lists

    listname : string
        Name of the list grouping variable

    subjconds : list
        List of subject conditions (str) to plot

    listconds : list
        List of list conditions (str) to plot

    plot_type : string
        Specifies the type of plot. If list (default), the list groupings (listgroup)
        will determine the plot grouping. If subject, the subject groupings
        (subjgroup) will determine the plot grouping. If split (currenty just
        works for accuracy plots), both listgroup and subjgroup will determine
        the plot groupings

    plot_style : string
        Specifies the style of the plot.  This currently works only for
        accuracy and fingerprint plots. The plot style can be bar (default for
        accruacy plot), violin (default for fingerprint plots) or swarm.

    title : string
        The title of the plot

    legend : bool
        If true (default), a legend is plotted.

    ylim : list of numbers
        A ymin/max can be specified by a list of the form [ymin, ymax]

    xlim : list of numbers
        A xmin/max can be specified by a list of the form [xmin, xmax]

    save_path : str
        Path to save out figure.  Include the file extension, e.g.
        save_path='figure.pdf'


    Returns
    ----------
    ax : matplotlib.Axes.Axis
        An axis handle for the figure

    """

    def plot_acc(data, plot_style, plot_type, listname, subjname, **kwargs):

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
            ax = plot_func(data=data, x=listname, y="Accuracy", **kwargs)
        elif plot_type is 'subject':
            ax = plot_func(data=data, x=subjname, y="Accuracy", **kwargs)
        elif plot_type is 'split':
            ax = plot_func(data=data, x=subjname, y="Accuracy", hue=listname, **kwargs)

        return ax

    def plot_temporal(data, plot_style, plot_type, listname, subjname, **kwargs):

        # set default style to bar
        plot_style = plot_style if plot_style is not None else 'bar'
        plot_type = plot_type if plot_type is not None else 'list'

        if plot_style is 'bar':
            plot_func = sns.barplot
        elif plot_style is 'swarm':
            plot_func = sns.swarmplot
        elif plot_style is 'violin':
            plot_func = sns.violinplot

        if plot_type is 'list':
            ax = plot_func(data=data, x=listname, y="Temporal Clustering Score", **kwargs)
        elif plot_type is 'subject':
            ax = plot_func(data=data, x=subjname, y="Temporal Clustering Score", **kwargs)
        elif plot_type is 'split':
            ax = plot_func(data=data, x=subjname, y="Temporal Clustering Score", hue=listname, **kwargs)

        return ax

    def plot_fingerprint(data, plot_style, plot_type, listname, subjname, **kwargs):

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

        return ax

    def plot_fingerprint_temporal(data, plot_style, plot_type, listname, subjname, **kwargs):

        # set default style to violin
        plot_style = plot_style if plot_style is not None else 'violin'
        plot_type = plot_type if plot_type is not None else 'list'

        if plot_style is 'bar':
            plot_func = sns.barplot
        elif plot_style is 'swarm':
            plot_func = sns.swarmplot
        elif plot_style is 'violin':
            plot_func = sns.violinplot

        order = list(tidy_data['Feature'].unique())
        order.remove('temporal')
        order = order + ['temporal']
        if plot_type is 'list':
            ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", hue=listname, order=order, **kwargs)
        elif plot_type is 'subject':
            ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", hue=subjname, order=order, **kwargs)
        else:
            ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", order=order, **kwargs)

        return ax

    def plot_spc(data, plot_style, plot_type, listname, subjname, **kwargs):

        plot_type = plot_type if plot_type is not None else 'list'

        if plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Proportion Recalled", unit="Subject", condition=subjname, **kwargs)
        elif plot_type is 'list':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Proportion Recalled", unit="Subject", condition=listname, **kwargs)
        ax.set_xlim(0, 15)

        return ax

    def plot_pnr(data, plot_style, plot_type, listname, subjname, position, **kwargs):

        plot_type = plot_type if plot_type is not None else 'list'

        print(data)

        if plot_type is 'subject':
            ax = sns.tsplot(data = data, time="Position", value='Probability of Recall: Position ' + str(position), unit="Subject", condition=subjname, **kwargs)
        elif plot_type is 'list':
            ax = sns.tsplot(data = data, time="Position", value='Probability of Recall: Position ' + str(position), unit="Subject", condition=listname, **kwargs)
        # ax.set_xlim(0,attrs['list_length']-1)

        return ax

    def plot_lagcrp(data, plot_style, plot_type, listname, subjname, **kwargs):

        plot_type = plot_type if plot_type is not None else 'list'

        if plot_type is 'subject':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Conditional Response Probability", unit="Subject", condition=subjname, **kwargs)
        elif plot_type is 'list':
            ax = sns.tsplot(data = tidy_data, time="Position", value="Conditional Response Probability", unit="Subject", condition=listname, **kwargs)
        ax.set_xlim(-5,5)

        return ax

    # if no grouping, set default to iterate over each list independently
    subjgroup = subjgroup if subjgroup is not None else results.data.index.levels[0].values
    listgroup = listgroup if listgroup is not None else results.data.index.levels[1].values

    if subjconds:
        # make sure its a list
        if type(subjconds) is not list:
            subjconds=[subjconds]

        # slice
        idx = pd.IndexSlice
        results.data = results.data.sort_index()
        results.data = results.data.loc[idx[subjconds, :],:]

        # filter subjgroup
        subjgroup = filter(lambda x: x in subjconds, subjgroup)

    if listconds:
        # make sure its a list
        if type(listconds) is not list:
            listconds=[listconds]

        # slice
        idx = pd.IndexSlice
        results.data = results.data.sort_index()
        results.data = results.data.loc[idx[:, listconds],:]

    # convert to tiny and format for plotting
    tidy_data = format2tidy(results.data, subjname, listname, subjgroup, analysis=results.analysis, position=results.position)

    #plot!
    if results.analysis is 'accuracy':
        ax = plot_acc(tidy_data, plot_style, plot_type, listname, subjname, **kwargs)
    elif results.analysis is 'temporal':
        ax = plot_temporal(tidy_data, plot_style, plot_type, listname, subjname, **kwargs)
    elif results.analysis is 'fingerprint':
        ax = plot_fingerprint(tidy_data, plot_style, plot_type, listname, subjname, **kwargs)
    elif results.analysis is 'fingerprint_temporal':
        ax = plot_fingerprint_temporal(tidy_data, plot_style, plot_type, listname, subjname, **kwargs)
    elif results.analysis is 'spc':
        ax = plot_spc(tidy_data, plot_style, plot_type, listname, subjname, **kwargs)
    elif results.analysis is 'pfr' or results.analysis is 'pnr':
        ax = plot_pnr(tidy_data, plot_style, plot_type, listname, subjname, position=results.position, **kwargs)
    elif results.analysis is 'lagcrp':
        ax = plot_lagcrp(tidy_data, plot_style, plot_type, listname, subjname, **kwargs)

    # add title
    if title:
        plt.title(title)

    if legend is False:
        try:
            ax.legend_.remove()
        except:
            pass

    if xlim:
        plt.xlim(xlim)

    if ylim:
        plt.ylim(ylim)

    if save_path:
        plt.savefig(save_path)

    plt.show()

    return ax
