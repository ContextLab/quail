.. sample documentation master file, created by
   sphinx-quickstart on Mon Apr 16 21:22:43 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**Quail**: A python toolbox for analyzing free recall experiments and plotting the results
====================================================================================================

.. image:: _static/murdock_1962_analysis.png
    :width: 800pt
    :align: center
    :alt: Murdock (1962) Free Recall Analysis

`Quail <https://github.com/ContextLab/quail>`_ is a library for analyzing and visualizing free recall data
in Python. It is built on top of matplotlib and seaborn.  For sample Jupyter
notebooks, click `Examples <https://github.com/ContextLab/quail-example-notebooks>`_
and to read the paper, click
`Paper <http://joss.theoj.org/papers/3fb5123eb2538e06f6a25ded0a088b73>`_.

 Some key features of Quail are:

 + A simple data structure for encoding and recall data (eggs).
 + A set of functions for analyzing data: accuracy, serial position curves, p(first recall), lag-crp and memory fingerprints!
 + Simple API for customizing plot styles.
 + Set of powerful tools for importing data, automatically transcribing audio files and more.

 .. toctree::
    :maxdepth: 2
    :caption: Contents:

    installation
    tutorial
    auto_examples/index
    api
