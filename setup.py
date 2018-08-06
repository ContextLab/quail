# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

DESCRIPTION = 'A python toolbox for analyzing and plotting free recall data'
LONG_DESCRIPTION = """\
Quail is a Python package that facilitates analyses of behavioral data from memory experiments. (The current focus is on free recall experiments.) Key features include:

- Serial position curves (probability of recalling items presented at each presentation position)
Probability of Nth recall curves (probability of recalling items at each presentation position as the Nth recall in the recall sequence)
- Lag-Conditional Response Probability curves (probability of transitioning between items in the recall sequence, as a function of their relative presentation positions)
- Clustering metrics (e.g. single-number summaries of how often participants transition from recalling a word to another related word, where "related" can be user-defined.)
- Many nice plotting functions
- Convenience functions for loading in data
- Automatically parse speech data (audio files) using wrappers for the Google Cloud Speech to Text API

The intended user of this toolbox is a memory researcher who seeks an easy way to analyze and visualize data from free recall psychology experiments.
"""

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

EXTRAS_REQUIRE={
    'speech-decoding': ["pydub", "google-cloud-speech<0.31dev,>=0.30.0", "google-cloud>=0.32.0,<0.34.0"],
    'efficient-learning': ["sqlalchemy"],
}

setup(
    name='quail',
    version='0.2.0',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Contextual Dynamics Lab',
    author_email='contextualdynamics@gmail.com',
    url='https://github.com/ContextLab/quail',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs', 'paper')),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
)
