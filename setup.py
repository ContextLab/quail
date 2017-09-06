# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


long_description=""" \
Quail is a Python package that facilitates analyses of behavioral data from memory experiments. (The current focus is on free recall experiments.) Key features include:
- Serial position curves (probability of recalling items presented at each presentation position)
- Probability of Nth recall curves (probability of recalling items at each presentation position as the Nth recall in the recall sequence)
- Lag-Conditional Response Probability curves (probability of transitioning between items in the recall sequence, as a function of their relative presentation positions)
- Clustering metrics (e.g. single-number summaries of how often participants transition from recalling a word to another related word, where "related" can be user-defined.)
- Many nice plotting functions
- Convenience functions for loading in data
- Automatically parse speech data (audio files) using wrappers for the Google Cloud Speech to Text API

For API documentation, examples and tutorials: http://cdl-quail.readthedocs.io/en/latest/
For sample Jupyter notebooks using the package: https://github.com/ContextLab/quail-example-notebooks
"""

with open('LICENSE') as f:
    license = f.read()

setup(
    name='quail',
    version='0.1.2',
    description='A python toolbox for analyzing and plotting free recall data',
    long_description=long_description,
    author='Contextual Dynamics Lab',
    author_email='contextualdynamics@gmail.com',
    url='https://github.com/ContextLab/quail',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'paper')),
    include_package_data=True,
    install_requires=[
        "seaborn>=0.7.1",
        "matplotlib>=1.5.1",
        "scipy>=0.17.1",
        "numpy>=1.10.4",
        "pandas>=0.20.3",
        "sqlalchemy",
        "dill",
        "requests",
        "pydub",
        "google-cloud-speech",
        "multiprocessing",
        "pathos",
        "future"
    ]
)
