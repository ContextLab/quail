from __future__ import division
import numpy as np
import pandas as pd
import seaborn as sns
from .helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42

def plot(data, subjgroup=None, subjname='Subject Group', listgroup=None,
         listname='List', subjconds=None, listconds=None, plot_type=None,
         plot_style=None, title=None, legend=True, xlim=None, ylim=None, save_path=None,
         **kwargs):
    """
    General plot function that groups data by subject/list number and performs analysis.

    Parameters
    ----------
    data : Pandas DataFrame or list of Pandas DataFrames
        The result of a quail analysis

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
    if type(data) is not list:
        data=[data]

    for d in data:

        attrs = d.attrs

        # if no grouping, set default to iterate over each list independently
        subjgroup = subjgroup if subjgroup is not None else d.index.levels[0].values
        listgroup = listgroup if listgroup is not None else d.index.levels[1].values

        if subjconds:
            # make sure its a list
            if type(subjconds) is not list:
                subjconds=[subjconds]

            # slice
            idx = pd.IndexSlice
            d = d.sort_index()
            d = d.loc[idx[subjconds, :],:]

            # filter subjgroup
            subjgroup = filter(lambda x: x in subjconds, subjgroup)

        if listconds:
            # make sure its a list
            if type(listconds) is not list:
                listconds=[listconds]

            # slice
            idx = pd.IndexSlice
            d = d.sort_index()
            d = d.loc[idx[:, listconds],:]

        # convert to tiny and format for plotting
        tidy_data = format2tidy(d, subjname, listname, subjgroup, **attrs)

        #plot!
        if attrs['analysis_type'] is 'accuracy':

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

        elif attrs['analysis_type'] is 'temporal':

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
                ax = plot_func(data=tidy_data, x=listname, y="Temporal Clustering Score", **kwargs)
            elif plot_type is 'subject':
                ax = plot_func(data=tidy_data, x=subjname, y="Temporal Clustering Score", **kwargs)
            elif plot_type is 'split':
                ax = plot_func(data=tidy_data, x=subjname, y="Temporal Clustering Score", hue=listname, **kwargs)

        elif attrs['analysis_type'] is 'fingerprint' or attrs['analysis_type'] is 'fingerprint_temporal':

            # set default style to violin
            plot_style = plot_style if plot_style is not None else 'violin'
            plot_type = plot_type if plot_type is not None else 'list'

            if plot_style is 'bar':
                plot_func = sns.barplot
            elif plot_style is 'swarm':
                plot_func = sns.swarmplot
            elif plot_style is 'violin':
                plot_func = sns.violinplot

            if attrs['analysis_type'] is 'fingerprint':
                if plot_type is 'list':
                    ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", hue=listname, **kwargs)
                elif plot_type is 'subject':
                    ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", hue=subjname, **kwargs)
                else:
                    ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", **kwargs)
            else:
                # move order to the end
                order = list(tidy_data['Feature'].unique())
                order.remove('temporal')
                order = order + ['temporal']
                if plot_type is 'list':
                    ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", hue=listname, order=order, **kwargs)
                elif plot_type is 'subject':
                    ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", hue=subjname, order=order, **kwargs)
                else:
                    ax = plot_func(data=tidy_data, x="Feature", y="Clustering Score", order=order, **kwargs)

        elif attrs['analysis_type'] is 'spc':

            plot_type = plot_type if plot_type is not None else 'list'

            if plot_type is 'subject':
                ax = sns.tsplot(data = tidy_data, time="Position", value="Proportion Recalled", unit="Subject", condition=subjname, **kwargs)
            elif plot_type is 'list':
                ax = sns.tsplot(data = tidy_data, time="Position", value="Proportion Recalled", unit="Subject", condition=listname, **kwargs)
            ax.set_xlim(0,attrs['list_length']-1)

        elif attrs['analysis_type'] is 'pfr' or attrs['analysis_type'] is 'pnr':
            n=attrs['n']
            del attrs['n']

            plot_type = plot_type if plot_type is not None else 'list'

            if plot_type is 'subject':
                ax = sns.tsplot(data = tidy_data, time="Position", value='Probability of Recall: Position ' + str(n), unit="Subject", condition=subjname, **kwargs)
            elif plot_type is 'list':
                ax = sns.tsplot(data = tidy_data, time="Position", value='Probability of Recall: Position ' + str(n), unit="Subject", condition=listname, **kwargs)
            ax.set_xlim(0,attrs['list_length']-1)

        if attrs['analysis_type']=='lagcrp':

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

        if xlim:
            plt.xlim(xlim)

        if ylim:
            plt.ylim(ylim)

        if save_path:
            plt.savefig(save_path)

        plt.show()

    return ax
